"""
Converssão de volume e densidade para a temperatura
de referência de derivados de petroleo
"""

from configparser import ConfigParser  # Ler o arquivo de configuração
import ast  # Transformar literal em lista
import numpy as np
import numpy.typing as npt
from typing import cast, Dict, Optional
from pydantic import BaseModel, validator  # Validação de dados
from pydantic.fields import ModelField

__all__ = ['DerConverter']


class DerParametros:
    """Recupera os pametros do modelo do arquivo de inicilaização"""

    def __init__(self) -> None:
        config = ConfigParser()
        config.read(f"{__file__[:-9]}config_parameters.ini")
        self.den_inf = np.array(ast.literal_eval(config["Derivados"]["den_inf"]))
        self.den_sup = np.array(ast.literal_eval(config["Derivados"]["den_sup"]))
        self.tab1a = np.array(ast.literal_eval(config["Derivados"]["tab1a"]))
        self.tab2a = np.array(ast.literal_eval(config["Derivados"]["tab2a"]))
        self.tab1b = np.array(ast.literal_eval(config["Derivados"]["tab1b"]))
        self.tab2b = np.array(ast.literal_eval(config["Derivados"]["tab2b"]))
        self.li_temp = float(config["Derivados"]["li_temp"])
        self.ls_temp = float(config["Derivados"]["ls_temp"])
        self.li_den = float(config["Derivados"]["li_den"])
        self.ls_den = float(config["Derivados"]["ls_den"])


class DerConverter(BaseModel):
    """Classe para convesão de volume"""

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True  # Por causa da classe DerParametros

    parametros: DerParametros = DerParametros()
    temp_amostra: Optional[float]
    dens_amostra: Optional[float]
    temp_ct: Optional[float]

    @validator("temp_amostra", "temp_ct")
    @classmethod
    def limite_temp(
        cls, value: float, values: Dict[str, DerParametros], field: ModelField
    ) -> float:
        """ Valida os limites da temperatura """
        if value < values["parametros"].li_temp:
            raise ValueError(
                f"A {field.name} deve ser menor"
                f" ou iguala a {values['parametros'].li_temp} °C"
            )
        if value > values["parametros"].ls_temp:
            raise ValueError(
                f"A {field.name} deve ser maior"
                f" ou iguala a {values['parametros'].ls_temp} °C"
            )
        return value

    @validator("dens_amostra")
    @classmethod
    def limite_den(
        cls, value: float, values: Dict[str, DerParametros], field: ModelField
    ):
        """ Valida os limites da densidade """
        if value < values["parametros"].li_den:
            raise ValueError(
                f"A {field.name} deve ser menor"
                f" ou iguala a {values['parametros'].li_den} g/cm³"
            )
        if value > values["parametros"].ls_den:
            raise ValueError(
                f"A {field.name} deve ser maior"
                f" ou iguala a {values['parametros'].ls_den} g/cm³"
            )
        return value

    @staticmethod
    def _hyc_derivados(temp_amostra: float) -> float:
        """Retorna a correção do densimetro de vidro do modelo de derivados"""

        result = 1 - 0.000023 * (temp_amostra - 20)
        result -= 0.00000002 * pow((temp_amostra - 20), 2)
        return result

    def _get_tab_derivados(
        self, dens_amostra: float, tab: npt.NDArray[np.float32]
    ) -> float:
        """Retorna o parametro do derivado da tabela em função da dens_amostra"""

        # Usa o campo den_inf para filtrar as outras tabelas
        filtro1: np.bool8 = self.parametros.den_inf < dens_amostra
        filtro2: np.bool8 = self.parametros.den_sup >= dens_amostra
        filtro: np.bool8 = filtro1 & filtro2
        return cast(float, tab[filtro][0])

    def _p1_derivados(self, dens_amostra: float) -> float:
        """Retona o paremetro p1 do modelo de derivados"""

        # Recupera so dados das tabelas em função da densidade
        t1a = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab1a
        )
        t2a = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2a
        )
        t1b = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab1b
        )
        t2b = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2b
        )

        # Cálculo do parmetro P1 do modelo
        result = t1a + 16 * t1b
        result_int = 8 * t1a + 64 * t1b
        result_int *= t2a + 16 * t2b
        result_int /= 1 + 8 * t2a + 64 * t2b
        result -= result_int
        result *= (9 / 5) * 0.999042
        return result

    def _p2_derivados(self, dens_amostra: float) -> float:
        """Retona o paremetro p2 do modelo de derivados"""

        # Recupera so dados das tabelas em função da densidade
        t2a = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2a
        )
        t2b = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2b
        )

        # Cálculo do parmetro P2 do modelo
        result = (9 / 5) * (t2a + 16 * t2b)
        result /= 1 + 8 * t2a + 64 * t2b
        return result

    def _p3_derivados(self, dens_amostra: float) -> float:
        """Retona o paremetro p3 do modelo de derivados"""

        # Recupera so dados das tabelas em função da densidade
        t1a = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab1a
        )
        t2a = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2a
        )
        t1b = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab1b
        )
        t2b = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2b
        )

        # Cálculo do parmetro P3 do modelo
        result = -((8 * t1a + 64 * t1b) * t2b)
        result /= 1 + 8 * t2a + 64 * t2b
        result += t1b
        result *= 81 / 25 * 0.999042
        return result

    def _p4_derivados(self, dens_amostra: float) -> float:
        """Retona o paremetro p4 do modelo de derivados"""

        # Recupera so dados das tabelas em função da densidade
        t2a = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2a
        )
        t2b = self._get_tab_derivados(
            dens_amostra=dens_amostra, tab=self.parametros.tab2b
        )

        # Cálculo do parmetro P4 do modelo
        result = 81 / 25 * (t2b / (1 + 8 * t2a + 64 * t2b))
        return result

    def dens20(self, temp_amostra: float, dens_amostra: float) -> float:
        """Retorna a densidade a 20 de derivados"""

        # Dipara a validação
        self.temp_amostra = temp_amostra
        self.dens_amostra = dens_amostra
        temp_amostra = self.temp_amostra
        dens_amostra = self.dens_amostra

        # Calculo dos parâmetros do modelo
        p1_calc = self._p1_derivados(dens_amostra=dens_amostra)
        p2_calc = self._p2_derivados(dens_amostra=dens_amostra)
        p3_calc = self._p3_derivados(dens_amostra=dens_amostra)
        p4_calc = self._p4_derivados(dens_amostra=dens_amostra)
        hyc_cal = self._hyc_derivados(temp_amostra=temp_amostra)

        # Cálculo da densidade dos devivados
        result_num = dens_amostra - p1_calc * (temp_amostra - 20.0)
        result_num = result_num - p3_calc * pow(temp_amostra - 20.0, 2)
        result_den = 1 + p2_calc * (temp_amostra - 20)
        result_den = result_den + p4_calc * pow(temp_amostra - 20.0, 2)
        result = result_num / result_den
        result = result * hyc_cal  # Correção do densímetro de vidro
        return round(result, 6)

    def fator(
        self,
        temp_amostra: float,
        dens_amostra: float,
        temp_ct: float,
    ) -> float:
        """Retorna o fator de converssap de derivados"""

        # Dipara a validação
        self.temp_amostra = temp_amostra
        self.dens_amostra = dens_amostra
        self.temp_ct = temp_ct
        temp_amostra = self.temp_amostra
        dens_amostra = self.dens_amostra
        temp_ct = self.temp_ct

        # Calculo dos parâmetros do modelo
        p1_calc = self._p1_derivados(dens_amostra=dens_amostra)
        p2_calc = self._p2_derivados(dens_amostra=dens_amostra)
        p3_calc = self._p3_derivados(dens_amostra=dens_amostra)
        p4_calc = self._p4_derivados(dens_amostra=dens_amostra)

        # Cálculo do fator de converssão dos derivados
        result_par1 = 1 + p2_calc * (temp_ct - 20.0)
        result_par1 += p4_calc * pow((temp_ct - 20.0), 2)
        result_par2 = p1_calc * (temp_ct - 20.0)
        result_par2 += p3_calc * pow((temp_ct - 20.0), 2)
        result_par2 /= self.dens20(dens_amostra=dens_amostra, temp_amostra=temp_amostra)
        return round(result_par1 + result_par2, 6)
