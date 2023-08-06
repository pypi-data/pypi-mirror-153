# volcon

Este é um pacote usado para converssão de volume de derivados de petróleo

Este pacote tem um proposito academico, assim não deve ser usados para converssões reais

## Instalação

Execute o seguinte para instlar:

```python
pip install volder
```

## Uso

```python
from volder.volder import DerConverter

der_conv = DerConverterr()
dens20 =  der_conv.dens20(temp_amostra=32.3, dens_amostra=0.8234)
```

## Desenvolvimento

Para instalar volconv junto com as ferramentas para desenvolver e realizar testes,
use o seguinte comando:

```python
pip install -e .[dev]
```