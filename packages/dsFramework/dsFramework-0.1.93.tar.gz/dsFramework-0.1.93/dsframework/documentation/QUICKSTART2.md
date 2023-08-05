## Part 2 - Project setup - Setting up a new project.{#quick_start2} 

&nbsp;
### step 1 - Setting up your inputs and outputs data variables.
What data variables you need as an input? it could be a dataset or part of it and additional required variables, such
as threshold etc.

* Set it in **pipeline/schema/<my-new-project>Inputs.py** file.

a couple of examples:
```
class <my-new-project>Inputs(BaseModel):
    email: str = ""
    threshold: Optional[float]
    hints: Optional[List[EmailHint]]
```

or

```
class <my-new-project>Inputs(BaseModel):
    html_content: str
    source: str
    queue_name: str
    title: str
``` 

or

```
class <my-new-project>Inputs(BaseModel):
    signatures: List[Signature]
    
```

<br />
What are the expected variables to output?
* Set it in **pipeline/schema/<my-new-project>Outputs.py** file.

for example:
```
class <my-new-project>Outputs(BaseModel):
    is_valid: int = 0
    prob: float = 0.5
    version: str
```

or

```
class <my-new-project>Outputs(BaseModel):
    pred: bool
    prob: float
    version: str = ''
```


&nbsp;
### step 2 - Load the artifacts 

Edit the config file, located here: 
  * <my-new-project>/config/config.json
  
```
"artifacts": [
    {"name":"" ,"path": "", "type": ""}
]
```
for example:
```
{"name":"buzzwords" ,"path": "pipeline/artifacts/vocabs/buzzwords.json", "type": "json"}
```
or
```
{"name":"rf_model" ,"path": "pipeline/artifacts/models/rf_clf_model_1000trees.pkl", "type": "pickle"}
```
Specify the following:
name: Any name
path: Relative path to the model.
type: "json", "csv", "pickle", "tensorflow" - for additional types check SharedArtifacts class (shared_artifacts.py).

### step 3 - Setting up the predictor
Run predict dataset in this step.

By default, the project is created to return the same predictables object as it received without prediction,
as you can see the execute method in the file <my-new-project>/pipeline/predictors/predictor.py here:
```
def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
    return predictables
```

To predict a dataset run it by the model, as you can see in this example:
```
def execute(self, predictables: List[Any], **kwargs) -> List[Any]:    
    features = [list(vars(p.features).values()) for p in predictables]
    
    results = self.artifacts.rf_model.predict_proba(features)
    
    idx = 0
    for p in predictables:
        p.prob = results[idx][-1]
        idx += 1
    
    return predictables
```
or
```
def execute(self, predictables: List[Any], **kwargs) -> List[Any]:
            
    predictables.results = self.artifacts.model(predictables.data)
        
    return predictables
```


&nbsp;
### step 4 - Preprocess
The preprocess step main purpose is where we run all pre-process procedures, by default it is set to 
throw a NotImplemented exception, see here:
```
    def preprocess(self, raw_input: Any):        
        raise NotImplementedError
```

For the project to run (even before adding any preprocess procedures), you can return it the way it was received:
```
    def preprocess(self, raw_input: Any):
        return raw_input        
``` 
Set it in the following file:
<my-new-project>/pipeline/preprocessor/preprocess.py

&nbsp;
### step 5 - Postprocess
Similar to the previous step the method postprocess main purpose is where we run all post-process procedures and by 
default it is set to throw a NotImplemented exception.

Set it in the following file:
<my-new-project>/pipeline/postprocessor/postprocess.py

for example:
```
    def get_output_objet(self, predictable):
        prob = predictable[-1]
        pred = False
        if prob > self.artifacts.threshold:
            pred = True

        return <my-new-project>Outputs(pred=pred, prob=prob)
```

