from edc_auth.site_auths import site_auths

from .auth_objects import MNSI, MNSI_SUPER, MNSI_VIEW, mnsi_codenames

site_auths.add_group(*mnsi_codenames, name=MNSI_VIEW, view_only=True)
site_auths.add_group(*mnsi_codenames, name=MNSI, no_delete=True)
site_auths.add_group(*mnsi_codenames, name=MNSI_SUPER)
