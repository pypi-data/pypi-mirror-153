from edc_lab import RequisitionPanel

from .processing_profiles import (
    csf_chem_processing_profile,
    csf_pkpd_processing_profile,
    csf_stop_processing_profile,
    csf_store_processing_profile,
    qpcr_csf_processing_profile,
)

csf_chemistry_panel = RequisitionPanel(
    name="csf_chem_haem_routine",
    verbose_name="CSF Chem and Haem Routine",
    processing_profile=csf_chem_processing_profile,
)

csf_pkpd_panel = RequisitionPanel(
    name="csf_pk_pd",
    verbose_name="CSF PK/PD",
    processing_profile=csf_pkpd_processing_profile,
)

qpcr_csf_panel = RequisitionPanel(
    name="qpcr_csf",
    verbose_name="qPCR CSF",
    processing_profile=qpcr_csf_processing_profile,
)

csf_panel = RequisitionPanel(
    name="csf_test_and_store",
    verbose_name="CSF Test and Store",
    processing_profile=csf_store_processing_profile,
)

csf_stop_panel = RequisitionPanel(
    name="csf_stop_cm",
    verbose_name="CSF STOP-CM",
    processing_profile=csf_stop_processing_profile,
)
