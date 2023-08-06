from ftw.upgrade import UpgradeStep


class FixRegistryFieldFrontendEdit(UpgradeStep):
    """Fix registry field frontend edit.
    """

    def __call__(self):
        self.install_upgrade_profile()
