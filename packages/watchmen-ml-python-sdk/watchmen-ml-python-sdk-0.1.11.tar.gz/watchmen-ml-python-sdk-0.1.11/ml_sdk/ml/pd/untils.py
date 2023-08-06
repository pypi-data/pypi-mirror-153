from ml_sdk.ml.model.factor_type import FactorType


def convert_to_pandas_type(factor_type: FactorType) -> str:
    if factor_type in [FactorType.NUMBER, FactorType.UNSIGNED, FactorType.SEQUENCE]:
        return 'float64'
    elif factor_type in [
        FactorType.YEAR, FactorType.HALF_YEAR, FactorType.QUARTER,
        FactorType.MONTH, FactorType.HALF_MONTH, FactorType.TEN_DAYS,
        FactorType.WEEK_OF_YEAR, FactorType.WEEK_OF_MONTH, FactorType.HALF_WEEK,
        FactorType.DAY_OF_MONTH, FactorType.DAY_OF_WEEK, FactorType.DAY_KIND,
        FactorType.HOUR, FactorType.HOUR_KIND, FactorType.MINUTE, FactorType.SECOND,
        FactorType.MILLISECOND, FactorType.AM_PM]:
        return 'float64'
    elif factor_type in [FactorType.FULL_DATETIME, FactorType.DATETIME, FactorType.DATE, FactorType.DATE_OF_BIRTH]:
        return 'datetime64'
    elif factor_type == FactorType.BOOLEAN:
        return 'bool'
    else:
        return 'object'
