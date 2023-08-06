# Build "Classic"

<br>

Forma "padrão" para buildar um python package no PyPi

<br>

A coisa mais simples é o _build_ localmente!

```
python setup.py build
```

<br>

---

## Distribuição do Pacote

### sdist

Uma dos formas de distribuição de pacotes é por meio do arquivo _tar.gz_. Para isso, basta criar com:

```
python setup.py sdist
```

### wheel

Há também o formato wheel

```
python setup.py bdist_wheel
python setup.py sdist bdist_wheel # Fazer ambos
```

---

## Publicação do Pacote

Por meio do twine é possível fazer o upload para o PyPI.

### Twine

```
twine upload dist/*
```

<br>

---

## Instalação

Para instalar localmente...
... usei para testar o _entry point_.

```
python setup.py install
```

<br>

---

## Setup File

- https://github.com/huggingface/evaluate/blob/main/setup.py

<br>

---

### VENV

ror: [Errno 1] Operation not permitted: 'lib' -> '/home/michel/Codes/open_traquitanas/build_classic/venv/lib64'

```
python -m venv ./venv
```

https://stackoverflow.com/questions/28651173/virtualenv-returns-error-operation-not-permitted
