use ethereum_pyspec_db::{Account, MutableTransaction, DB};
use ethereum_types::{Address, H256, U256};
use std::path::Path;

#[no_mangle]
pub extern "C" fn open(path: *const u8, path_len: usize) -> *mut () {
    let slice: &[u8] = unsafe { std::slice::from_raw_parts(path, path_len) };
    let path = Path::new(std::str::from_utf8(slice).unwrap());
    Box::into_raw(Box::new(DB::open(path).unwrap())).cast()
}

#[no_mangle]
pub extern "C" fn open_in_memory() -> *mut () {
    Box::into_raw(Box::new(DB::open_in_memory().unwrap())).cast()
}

#[no_mangle]
pub extern "C" fn drop_db(db: *mut ()) {
    let db: Box<DB> = unsafe { Box::from_raw(db.cast()) };
    drop(db)
}

#[no_mangle]
pub extern "C" fn begin_mutable(db: *mut ()) -> *mut () {
    let db: &mut DB = unsafe { &mut *db.cast() };
    Box::into_raw(Box::new(db.begin_mutable().unwrap())).cast()
}

#[no_mangle]
pub extern "C" fn commit_mutable(tx: *mut ()) {
    let tx: Box<MutableTransaction> = unsafe { Box::from_raw(tx.cast()) };
    tx.commit().unwrap()
}

#[no_mangle]
pub extern "C" fn rollback_mutable(tx: *mut ()) {
    let tx: Box<MutableTransaction> = unsafe { Box::from_raw(tx.cast()) };
    drop(tx)
}

#[no_mangle]
pub extern "C" fn set_metadata(
    tx: *mut (),
    key: *const u8,
    key_len: usize,
    value: *const u8,
    value_len: usize,
) {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let key = unsafe { std::slice::from_raw_parts(key, key_len) };
    let value = unsafe { std::slice::from_raw_parts(value, value_len) };
    tx.set_metadata(key, value).unwrap()
}

#[repr(C)]
pub struct CGetMetadata {
    exists: bool,
    value: *const u8,
    value_len: usize,
}

static mut METADATA_CELL: Vec<u8> = Vec::new();

#[no_mangle]
pub extern "C" fn get_metadata(tx: *mut (), key: *const u8, key_len: usize) -> CGetMetadata {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let key = unsafe { std::slice::from_raw_parts(key, key_len) };
    match tx.get_metadata(key).unwrap() {
        None => CGetMetadata {
            exists: false,
            value: std::ptr::null(),
            value_len: 0,
        },
        Some(metadata) => unsafe {
            METADATA_CELL = metadata.to_vec();
            CGetMetadata {
                exists: true,
                value: METADATA_CELL.as_ptr(),
                value_len: METADATA_CELL.len(),
            }
        },
    }
}

static mut STATE_ROOT_CELL: H256 = H256::zero();

#[no_mangle]
pub extern "C" fn state_root(tx: *mut ()) -> *const u8 {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    unsafe {
        STATE_ROOT_CELL = tx.state_root().unwrap();
        STATE_ROOT_CELL.as_ptr()
    }
}

static mut STORAGE_ROOT_CELL: H256 = H256::zero();

#[no_mangle]
pub extern "C" fn storage_root(tx: *mut (), address: *const u8) -> *const u8 {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    unsafe {
        STORAGE_ROOT_CELL = tx.storage_root(&address).unwrap();
        STORAGE_ROOT_CELL.as_ptr()
    }
}

#[no_mangle]
pub extern "C" fn set_account_none(tx: *mut (), address: *const u8) {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    tx.set_account(address, None)
}

#[no_mangle]
pub extern "C" fn set_account_some(
    tx: *mut (),
    address: *const u8,
    nonce: u64,
    balance: *const u8,
    code: *const u8,
    code_len: usize,
) {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    let balance = U256::from_big_endian(unsafe { std::slice::from_raw_parts(balance, 32) });
    let code = unsafe { std::slice::from_raw_parts(code, code_len) }.to_vec();
    let code_hash = tx.store_code(&code).unwrap();
    tx.set_account(
        address,
        Some(Account {
            nonce,
            balance: balance.try_into().unwrap(),
            code_hash,
        }),
    )
}

#[repr(C)]
pub struct CGetAccount {
    exists: bool,
    nonce: u64,
    balance: *const u8,
    code: *const u8,
    code_len: usize,
}

// This is hack to keep pointers alive
static mut BALANCE_CELL: [u8; 32] = [0; 32];
static mut CODE_CELL: Vec<u8> = Vec::new();

#[no_mangle]
pub extern "C" fn get_account_optional(tx: *mut (), address: *const u8) -> CGetAccount {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    let account = tx.get_account_optional(address).unwrap();
    match account {
        None => CGetAccount {
            exists: false,
            nonce: 0,
            balance: std::ptr::null(),
            code: std::ptr::null(),
            code_len: 0,
        },
        Some(account) => unsafe {
            CODE_CELL = tx.get_code(account.code_hash).unwrap().unwrap().to_vec();
            account.balance.to_big_endian(&mut BALANCE_CELL);
            CGetAccount {
                exists: true,
                nonce: account.nonce,
                balance: BALANCE_CELL.as_ptr(),
                code: CODE_CELL.as_ptr(),
                code_len: CODE_CELL.len(),
            }
        },
    }
}

#[no_mangle]
pub extern "C" fn set_storage(tx: *mut (), address: *const u8, key: *const u8, value: *const u8) {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    let key = H256::from_slice(unsafe { std::slice::from_raw_parts(key, 32) });
    let value = U256::from_big_endian(unsafe { std::slice::from_raw_parts(value, 32) });
    tx.set_storage(address, key, value).unwrap()
}

static mut STORAGE_CELL: [u8; 32] = [0; 32];

#[no_mangle]
pub extern "C" fn get_storage(tx: *mut (), address: *const u8, key: *const u8) -> *const u8 {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    let key = H256::from_slice(unsafe { std::slice::from_raw_parts(key, 32) });
    unsafe {
        tx.get_storage(address, key)
            .unwrap()
            .to_big_endian(&mut STORAGE_CELL);
        STORAGE_CELL.as_ptr()
    }
}

#[no_mangle]
pub extern "C" fn destroy_storage(tx: *mut (), address: *const u8) {
    let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    let address = Address::from_slice(unsafe { std::slice::from_raw_parts(address, 20) });
    tx.destroy_storage(address)
}

#[no_mangle]
pub extern "C" fn debug_dump(tx: *mut ()) {
    unimplemented!()
    //let tx: &mut MutableTransaction = unsafe { &mut *tx.cast() };
    //tx.debug_dump_db().unwrap();
}
