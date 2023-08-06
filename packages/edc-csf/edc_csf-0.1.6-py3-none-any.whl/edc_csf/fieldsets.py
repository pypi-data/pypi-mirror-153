def get_lp_fieldset():
    return (
        "LP",
        {
            "fields": (
                "reason_for_lp",
                "lp_datetime",
                "opening_pressure_measured",
                "opening_pressure",
                "closing_pressure",
                "csf_amount_removed",
            )
        },
    )


def get_csf_fieldset():
    return (
        "CSF",
        {
            "fields": (
                "csf_positive",
                "india_ink",
                "csf_crag_lfa",
                "sq_crag",
                "sq_crag_pos",
                "crf_crag_titre_done",
                "crf_crag_titre",
            )
        },
    )


def get_quantitative_culture_fieldset(requisition_field=None):
    fields = ["qc_assay_datetime", "quantitative_culture"]
    if requisition_field:
        fields.insert(0, requisition_field)
    return (
        "Quantitative Culture",
        {"fields": fields},
    )


def get_csf_culture_fieldset(requisition_field=None):
    fields = [
        "csf_culture_assay_datetime",
        "csf_culture",
        "other_csf_culture",
        "csf_wbc_cell_count",
        "differential_lymphocyte_count",
        "differential_lymphocyte_unit",
        "differential_neutrophil_count",
        "differential_neutrophil_unit",
        "csf_glucose",
        "csf_glucose_units",
        "csf_protein",
        "csf_crag",
        "csf_crag_immy_lfa",
    ]
    if requisition_field:
        fields.insert(0, requisition_field)
    return (
        "CSF culture",
        {"fields": fields},
    )


def get_biosynex_semi_quantitative_crag_fieldset():
    return (
        "Biosynex Semi-quantitative CrAg",
        {
            "fields": [
                "bios_crag",
                "crag_control_result",
                "crag_t1_result",
                "crag_t2_result",
            ]
        },
    )
