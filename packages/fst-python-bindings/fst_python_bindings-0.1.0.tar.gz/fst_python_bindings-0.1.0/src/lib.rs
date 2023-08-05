mod levenstein_dyn;

use levenstein_dyn::DynamicLevenshtein;
use pyo3::{prelude::*, types::PyIterator, exceptions};
use fst::{Map, MapBuilder, IntoStreamer};


#[pyclass]
struct FstMap {
    map: Map<Vec<u8>>,
}


#[pymethods]
impl FstMap {
    #[staticmethod]
    fn from_iter(iter: &PyIterator) -> PyResult<Self> {
        let mut builder = MapBuilder::memory();
        for item in iter {
            let item = item?;
            let (key, value): (&str, u64) = item.extract()?;
            builder.insert(key, value).map_err(|e| value_error(e, "Items must be in sorted order."))?;
        }
        let data = builder.into_inner()
            .map_err(|e| value_error(e, "Construction error E01"))?; // TODO: add more info
        let map = Map::new(data)
            .map_err(|e| value_error(e, "Construction error E02"))?;

        Ok(FstMap{map})
    }

    fn search_levenstein(&self, query: &str, distance: usize) -> PyResult<Vec<(String, u64)>> {
        let stream = self.map.search(DynamicLevenshtein::new(query, distance)).into_stream();
        stream.into_str_vec().map_err(|e| value_error(e, "Search error"))
    }
}

fn value_error(err: fst::Error, cause: &str) -> PyErr {
    PyErr::new::<exceptions::PyValueError, _>(format!("{}: {}", cause, err))
}


#[pymodule]
fn fst_python_bindings(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<FstMap>()?;
    Ok(())
}