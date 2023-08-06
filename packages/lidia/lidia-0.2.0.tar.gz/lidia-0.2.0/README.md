# Lidia

_Lightweight Instrument Display Interface for Aircraft_

lidia is a Python package for serving an aircraft instruments panel as a web page.

<!-- TODO: https://www.makeareadme.com/ -->

## Usage

```bash
lidia simulate

# if your Scripts folder isn't in Path:
python3 -m lidia simulate

# use other source
lidia simulink
```

Then open the served page in a browser, by default [localhost:5555](http://localhost:5555)

## Contributing

- All code should be formatted with `autopep8`
- All documentation should be formatted with Prettier
- To properly run as a module without building and installing, **cd into `src/`** and run `python3 -m lidia`

## Acknowledgements

This software was developed in [Dipartimento di Scienze e Tecnologie Aerospaziali (DAER)](https://www.aero.polimi.it/) of Politecnico di Milano

## License

[MIT](https://choosealicense.com/licenses/mit/)
