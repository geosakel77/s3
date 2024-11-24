from s3lib.s3engineslib import Engine, EngineCore


class ActionabilityMetricEngine(Engine):

    def __init__(self,config,target_organization=None, cti_product=None):
        super().__init__(config,target_organization,cti_product)

        self.engine_core= self.ActionabilityMetricCore(self.config,self.product)


    class ActionabilityMetricCore(EngineCore):
        def __init__(self,config,cti_product):
            super().__init__(config,cti_product)

