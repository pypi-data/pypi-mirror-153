use captcha_rs::{Captcha, CaptchaBuilder};
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use base64::decode;

#[pyclass(name="Captcha")]
struct PyCaptcha {
    pub captcha: Captcha
}

#[pymethods]
impl PyCaptcha {
    #[new]
    fn new(length: usize, width: u32, height: u32, dark_mode: bool, complexity: u32) -> Self {
        PyCaptcha {
            captcha: CaptchaBuilder::new()
                .length(length)
                .width(width)
                .height(height)
                .dark_mode(dark_mode)
                .complexity(complexity)
                .build()
        }
    }

    fn get_text(&self) -> PyResult<String> {
        Ok((&self.captcha.text).to_string())
    }

    fn get_bytes(&self, py: Python) -> PyResult<PyObject> {
        let decoded: Vec<u8> = decode(self.captcha.base_img.split(",").collect::<Vec<&str>>().last().unwrap()).unwrap();
        Ok(PyBytes::new(py, &*decoded).into())
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn captcha_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyCaptcha>()?;
    Ok(())
}