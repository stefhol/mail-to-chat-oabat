use anyhow::Result;
use eml_parser::{eml::Eml, EmlParser};
pub mod util;
fn main() -> Result<()> {
    let eml: Eml = EmlParser::from_file("pages/response_2.eml")?
        .ignore_body()
        .parse()?;
    println!("{:?}", eml.parse());
    Ok(())
}
