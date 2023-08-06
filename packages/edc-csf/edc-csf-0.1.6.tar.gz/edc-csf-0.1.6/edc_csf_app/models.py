from django.db import models
from django.db.models import PROTECT
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_lab.models import Panel
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow
from edc_visit_schedule.model_mixins import VisitCodeFieldsModelMixin


class Appointment(
    NonUniqueSubjectIdentifierFieldMixin, VisitCodeFieldsModelMixin, BaseUuidModel
):

    appt_datetime = models.DateTimeField(default=get_utcnow)

    class Meta(BaseUuidModel.Meta):
        pass


class SubjectVisit(
    NonUniqueSubjectIdentifierFieldMixin, VisitCodeFieldsModelMixin, BaseUuidModel
):

    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT, related_name="+")

    class Meta(BaseUuidModel.Meta):
        pass


class SubjectRequisition(
    NonUniqueSubjectIdentifierFieldMixin, VisitCodeFieldsModelMixin, BaseUuidModel
):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=models.PROTECT, related_name="+")

    panel = models.ForeignKey(Panel, on_delete=PROTECT)

    class Meta(BaseUuidModel.Meta):
        pass
