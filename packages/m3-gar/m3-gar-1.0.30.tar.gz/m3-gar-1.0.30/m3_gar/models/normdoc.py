from django.db import (
    models,
)

from m3_gar.base_models import (
    NormativeDocs as BaseNormativeDocs,
    NormativeDocsKinds as BaseNormativeDocsKinds,
    NormativeDocsTypes as BaseNormativeDocsTypes,
)
from m3_gar.models.util import (
    RegionCodeModelMixin,
    make_fk,
)


__all__ = ['NormativeDocsKinds', 'NormativeDocsTypes', 'NormativeDocs']


class NormativeDocsKinds(BaseNormativeDocsKinds):
    """
    Сведения по видам нормативных документов
    """
    class Meta:
        verbose_name = 'Вид нормативного документа'
        verbose_name_plural = 'Виды нормативных документов'

    def __str__(self):
        return self.name


class NormativeDocsTypes(BaseNormativeDocsTypes):
    """
    Сведения по типам нормативных документов
    """
    class Meta:
        verbose_name = 'Тип нормативного документа'
        verbose_name_plural = 'Типы нормативных документов'

    def __str__(self):
        return self.name


class NormativeDocs(BaseNormativeDocs, RegionCodeModelMixin):
    """
    Сведения о нормативном документе, являющемся основанием присвоения
    адресному элементу наименования
    """

    # Перегрузка поля, поскольку ФНС старательно игнорирует факт того, что orgname в файлах ГАР уже давно больше
    # 255 символов. Как правило, невалидные строки либо содержат переносы строк (которые мы уже научились правильно
    # вырезать в рамках загрузки), либо в записи перепутаны значения между name и orgname (такие записи вычленить и
    # скорректировать практически невозможно)
    orgname = models.CharField(
        max_length=400,
        verbose_name='Наименование органа создвшего нормативный документ',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Нормативный документ'
        verbose_name_plural = 'Нормативные документы'

    def __str__(self):
        return self.name


make_fk(NormativeDocs, 'type', to=NormativeDocsTypes)
make_fk(NormativeDocs, 'kind', to=NormativeDocsKinds)
