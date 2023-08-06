use pyo3::prelude::*;
use pyo3::types::{PyTuple};
use pyo3::wrap_pyfunction;
use pyo3::exceptions::{PyValueError,PyRuntimeError};

use std::{
    collections::HashMap,
    fs::File,
};

use randomprime;
use randomprime::{
    structs::GcDisc,
    patch_config::PatchConfig,
    reader_writer::Reader,
};
use dol_symbol_table::mp1_symbol;

enum Version
{
    NtscU0_00,
    NtscU0_01,
    NtscU0_02,
    NtscJ,
    NtscK,
    Pal,
}

fn version_from_str(s: String) -> Option<Version>
{
    match s.as_str() {
        "0-00" => Some(Version::NtscU0_00),
        "0-01" => Some(Version::NtscU0_01),
        "0-02" => Some(Version::NtscU0_02),
        "kor" => Some(Version::NtscK),
        "jap" => Some(Version::NtscJ),
        "pal" => Some(Version::Pal),
        _ => None,
    }
}

fn version_to_str(v: Version) -> Option<String>
{
    match v {
        Version::NtscU0_00 => Some("0-00".to_string()),
        Version::NtscU0_01 => Some("0-01".to_string()),
        Version::NtscU0_02 => Some("0-02".to_string()),
        Version::NtscK => Some("kor".to_string()),
        Version::NtscJ => Some("jap".to_string()),
        Version::Pal => Some("pal".to_string()),
    }
}


struct ProgressNotifier
{
    python_object: PyObject
}

impl ProgressNotifier
{
    fn new(python_object: PyObject) -> ProgressNotifier
    {
        ProgressNotifier {
            python_object: python_object,
        }
    }
    
    fn handle_pyresult(&mut self, py: Python, result: PyResult<PyObject>)
    {
        if !result.is_ok() {
            result.unwrap_err().print(py)
        }
    }
}

impl randomprime::structs::ProgressNotifier for ProgressNotifier
{
    fn notify_total_bytes(&mut self, total_size: usize)
    {
        let gil = Python::acquire_gil(); 
        let py = gil.python();
        let args = PyTuple::new(py, &[total_size]);
        self.handle_pyresult(py, self.python_object.call_method1(py, "notify_total_bytes", args));
    }

    fn notify_writing_file(&mut self, file_name: &randomprime::reader_writer::CStr, file_bytes: usize)
    {
        let gil = Python::acquire_gil(); 
        let py = gil.python();
        let args = (file_name.to_bytes(), file_bytes);
        self.handle_pyresult(py, self.python_object.call_method1(py, "notify_writing_file", args));
    }

    fn notify_writing_header(&mut self)
    {
        let gil = Python::acquire_gil(); 
        let py = gil.python();
        self.handle_pyresult(py, self.python_object.call_method0(py, "notify_writing_header"));
    }

    fn notify_flushing_to_disk(&mut self)
    {
        let gil = Python::acquire_gil(); 
        let py = gil.python();
        self.handle_pyresult(py, self.python_object.call_method0(py, "notify_flushing_to_disk"));
    }
}

/// Performs the patching with the given config.
#[pyfunction]
#[text_signature = "(config_json, progress_notifier, /)"]
fn patch_iso(config_json: String, progress_notifier: PyObject) -> PyResult<()> {
    let patch_config = PatchConfig::from_json(config_json.as_str())
        .map_err(|e| PyValueError::new_err(e))?;
    
    let pn = ProgressNotifier::new(progress_notifier);
    randomprime::patches::patch_iso(patch_config, pn)
        .map_err(|e| PyRuntimeError::new_err(e))?;

    Ok(())
}

/// Gets version of the given file
#[pyfunction]
#[text_signature = "(file_path, /)"]
fn get_iso_mp1_version(file_path: String) -> PyResult<Option<String>> {

    let input_iso_file = File::open(file_path.trim())
        .map_err(|e| PyValueError::new_err(format!("Failed to open {}: {}", file_path, e)))?;

    let input_iso = unsafe { memmap::Mmap::map(&input_iso_file) }
        .map_err(|e| PyValueError::new_err(format!("Failed to open {}: {}", file_path, e)))?;

    let mut reader = Reader::new(&input_iso[..]);

    let gc_disc: GcDisc = reader.read(());

    let version = match (&gc_disc.header.game_identifier(), gc_disc.header.disc_id, gc_disc.header.version) {
        (b"GM8E01", 0, 0) => Version::NtscU0_00,
        (b"GM8E01", 0, 1) => Version::NtscU0_01,
        (b"GM8E01", 0, 2) => Version::NtscU0_02,
        (b"GM8E01", 0, 48) => Version::NtscK,
        (b"GM8J01", 0, 0) => Version::NtscJ,
        (b"GM8P01", 0, 0) => Version::Pal,
        // (b"R3ME01", 0, 0) => Version::NtscUTrilogy,
        // (b"R3IJ01", 0, 0) => Version::NtscJTrilogy,
        // (b"R3MP01", 0, 0) => Version::PalTrilogy,
        _ => {
            return Ok(None)
        },
    };

    return Ok(version_to_str(version));
}


/// Gets the symbols for the given version
#[pyfunction]
#[text_signature = "(version, /)"]
fn get_mp1_symbols(version: String) -> PyResult<HashMap<String, Option<u32>>> {
    let v = match version_from_str(version) {
        None => Err(PyValueError::new_err("Unknown version")),
        Some(ver) => Ok(ver),
    }?;
    
    let mut result: HashMap<String, Option<u32>> = HashMap::new();
    macro_rules! add_symbol {
        ($sym:tt) => {
            {
                let s = mp1_symbol!($sym);
                result.insert(String::from($sym), match v {
                    Version::NtscU0_00    => s.addr_0_00,
                    Version::NtscU0_01    => s.addr_0_01,
                    Version::NtscU0_02    => s.addr_0_02,
                    Version::NtscK        => s.addr_kor,
                    Version::NtscJ        => s.addr_jap,
                    Version::Pal          => s.addr_pal,
                });
            }
        }
    }
    add_symbol!("UpdateHintState__13CStateManagerFf");
    add_symbol!("wstring_l__4rstlFPCw");
    add_symbol!("DisplayHudMemo__9CSamusHudFRC7wstringRC12SHudMemoInfo");
    
    add_symbol!("InitializePowerUp__12CPlayerStateFQ212CPlayerState9EItemTypei");
    add_symbol!("IncrPickUp__12CPlayerStateFQ212CPlayerState9EItemTypei");
    add_symbol!("DecrPickUp__12CPlayerStateFQ212CPlayerState9EItemTypei");

    // Layers
    add_symbol!("g_StateManager");
    add_symbol!("g_GameState");
    add_symbol!("StateForWorld__10CGameStateFUi");
    add_symbol!("SetLayerActive__16CWorldLayerStateFiib");
    
    Ok(result)
}



/// A Python module implemented in Rust.
#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(patch_iso, m)?)?;
    m.add_function(wrap_pyfunction!(get_mp1_symbols, m)?)?;
    m.add_function(wrap_pyfunction!(get_iso_mp1_version, m)?)?;
 
    Ok(())
}