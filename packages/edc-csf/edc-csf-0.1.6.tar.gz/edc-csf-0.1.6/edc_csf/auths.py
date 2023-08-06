from edc_auth.site_auths import site_auths

from .auth_objects import EDC_CSF, EDC_CSF_SUPER, EDC_CSF_VIEW, codenames

site_auths.add_group(*codenames, name=EDC_CSF_VIEW, view_only=True)
site_auths.add_group(*codenames, name=EDC_CSF, no_delete=True)
site_auths.add_group(*codenames, name=EDC_CSF_SUPER)
