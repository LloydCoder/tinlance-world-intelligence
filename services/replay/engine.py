from packages.contracts.replay import ReplayManifest
class ReplayEngine:
 def __init__(self,artifacts:dict[str,bytes]): self.artifacts=artifacts
 def replay(self,manifest:ReplayManifest)->tuple[bytes,...]:
  return tuple(self.artifacts[a] for a in manifest.artifact_ids if a in self.artifacts)
