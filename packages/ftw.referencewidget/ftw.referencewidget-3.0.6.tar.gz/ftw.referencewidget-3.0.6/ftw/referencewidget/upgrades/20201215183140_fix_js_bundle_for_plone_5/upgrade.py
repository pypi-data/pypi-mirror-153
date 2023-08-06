from ftw.upgrade import UpgradeStep
import pkg_resources


IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'

class FixJsBundleForPlone5(UpgradeStep):
    """Fix js bundle for plone 5.
    """

    def __call__(self):
        if IS_PLONE_5:
            self.install_upgrade_profile()
