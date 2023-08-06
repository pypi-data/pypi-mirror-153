from edc_lab import Process, ProcessingProfile

from .aliquot_types import (
    csf,
    csf_glucose,
    csf_pellet,
    csf_supernatant,
    csf_testing,
    qfc,
)

csf_store_processing_profile = ProcessingProfile(name="csf_culture", aliquot_type=csf)
process_qfc = Process(aliquot_type=qfc, aliquot_count=3)
process_csf_testing = Process(aliquot_type=csf_testing, aliquot_count=2)
csf_store_processing_profile.add_processes(process_qfc, process_csf_testing)

csf_stop_processing_profile = ProcessingProfile(name="csf_store", aliquot_type=csf)
csf_store = Process(aliquot_type=qfc, aliquot_count=2)
process_csf_testing = Process(aliquot_type=csf_testing, aliquot_count=1)
csf_stop_processing_profile.add_processes(csf_store, process_csf_testing)

csf_pkpd_processing_profile = ProcessingProfile(name="csf_pkpd", aliquot_type=csf)
process_csf_pkpd = Process(aliquot_type=csf, aliquot_count=2)
csf_pkpd_processing_profile.add_processes(process_csf_pkpd)

qpcr_csf_processing_profile = ProcessingProfile(name="qpcr_csf", aliquot_type=csf)
process_supernatant = Process(aliquot_type=csf_supernatant, aliquot_count=1)
process_pellet = Process(aliquot_type=csf_pellet, aliquot_count=1)
qpcr_csf_processing_profile.add_processes(process_supernatant, process_pellet)

csf_chem_processing_profile = ProcessingProfile(name="csf_chemistry", aliquot_type=csf)
process_csf_glucose = Process(aliquot_type=csf_glucose, aliquot_count=1)
