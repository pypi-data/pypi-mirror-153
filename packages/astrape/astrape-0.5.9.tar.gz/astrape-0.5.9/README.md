# ASTRAPE : A STrategic, Reproducible & Accessible Project and Experiment (Dev version)



<div align="right">
      <b>Creator : Woosog Benjamin Chay</b> 
</div>
<div align="right">
      <b>benchay1@gmail.com (preferred) / benchay@kaist.ac.kr</b> 
</div>
<br/>
<br/>

<div align="center">
      <b>dev-release (0.3.33) available</b> 
</div>
<div align="center">
      <code><font size=4>pip install astrape</code>
</div>
      

<div align="right">
      <a href="https://colab.research.google.com/drive/1VZCR84K2pzKpZoFGy3kp8vOZYAYyvQjJ?usp=sharing">colab tutorial (experiment)</a> <br/>
      <a href="https://github.com/benchay1999/astrape/blob/main/tutorial/project_tutorial.ipynb">tutorial.ipynb (full tutorial with project)</a>
</div>

**Updates: (Unchecked are in progress)**
- [x] Compatibility with other PyTorch-Lightning Models
- [x] Compatibility with sklearn-based models
- [x] Add AUROC metrics for classification tasks
- [x] Change method names in `Project` for better readability
- [x] Polish codes for better readability    
- [ ] Make documentation for astrape
- [ ] Update tutorials respecting full features of astrape

      
**********
[1. Overview](#1-overview) <br/>
[2. Project](#2-project) <br/>
[3. Experiment](#3-experiment) <br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-1. Specifying Models](#3-1-specifying-models)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-2. (Optional) Specifying Trainers](#3-2-optional-specifying-trainers)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-3. Fitting the Model](#3-3-fitting-the-model)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-4. Stacking Fitted Models](#3-4-stacking-fitted-models)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-5. Saving Models](#3-5-saving-models)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-6. Checking the Best Model Thus Far](#3-6-checking-the-best-model-thus-far)<br/>
&nbsp;&nbsp;&nbsp;&nbsp;[3-7. (Stratified) K-Fold Cross-Validation](#3-7-stratified-k-fold-cross-validation)
<br/>



**********
# 1. Overview
Astrape : [https://en.wikipedia.org/wiki/Astrape_and_Bronte](https://en.wikipedia.org/wiki/Astrape_and_Bronte)

Astrape is a package that would help you organize machine learning projects. It is written mostly in PyTorch Lightning([https://pytorchlightning.ai](https://pytorchlightning.ai)). 


:zap: Astrape :zap: :
- Automatically creates appropriate folders and files(e.g., model checkpoints, logs, etc.) related to your experiment. 
- All your experiments are logged to Tensorboard automatically.
- Enables you to define models easily.
- No more tedious magic commands.
- Can quickly apply simple baseline algorithms in order to verify that your data is indeed "statistically significant" enough for machine learning tasks.

![Outline of Astrape](https://github.com/benchay1999/astrape/blob/main/astrape_outline.jpg?raw=true)

"Project" and "Experiment" conspire up to the soul of Astrape. The term "Project" here refers to "all set of possible machine learning *experiments* for analyzing the given data". Wait, what is an *experiment* anyway? An *experiment* here means "a process of train/validation/test phase with certain random state acquired for all random operations such as splitting scheme, initialization scheme, etc.". "Experiment" is a collection of *experiments* with the same random state.

For stability's sake, you are tempted to (and should) conduct several "Experiments" with different random states to verify that your data analysis is indeed accurate. Astrape organizes such "Experiments" in a way that makes this sanity-checking process succinct and reproducible.



# 2. Project 



Features of **Project** include :
- Plotting the data 
- Plotting results among experiments
- Providing arrays for axes in plotting

Check details in the [full tutorial](https://github.com/benchay1999/astrape/blob/main/tutorial/project_tutorial.ipynb).
      
I will add descriptions of Project and colab tutorial before May 28.

# 3. Experiment

When using Astrape, we expect you to conduct all experiments inside the `experiment.Experiment` class. This class takes a number of parameters, and you can check the details in the [tutorial](https://colab.research.google.com/drive/1VZCR84K2pzKpZoFGy3kp8vOZYAYyvQjJ?usp=sharing). 

Once you declare an experiment, all random operations are governed by the same random seed you defined as a parameter for the experiment. When initialized (with a given random state) and the train/validation/test data are specified, you should now declare models for the task.

## 3-1. Specifying Models

Declare a model using `.set_model()` method. Astrape supports 1) multi-layer perceptron with all # of hidden units identical among layers (`MLP`), 2) multi-layer perceptron with # of hidden units contracting with given constant rate (`ContractingMLP`), 3) cutomizedcustomized multi-layer perceptron of which you can define numbera  of hidden units for each layer using list (`CustomMLP`), 4) VGG network (`VGG`), 5) UNet (`UNet`). The models mentioned in this paragraph are all `pytorch_lightning.LightningModules`.
 

> You can also declare sci-kit learn models and their variants(e.g., xgboost) as well using `.set_model()`. Astrape is compatible with sci-kit learn and PyTorch-lightning modules. 


## 3-2. (Optional) Specifying Trainers 

PyTorch Lightning uses `Trainer` for training, validating, and testing models. You can specify it using the `.set_trainer()` method with trainer configurations as parameters. If you don't, default values will be set for the `Trainer`. Check the [tutorial]([https://github.com/benchay1999/astrape/blob/main/tutorial/tutorial.ipynb](https://colab.research.google.com/drive/1VZCR84K2pzKpZoFGy3kp8vOZYAYyvQjJ?usp=sharing)) for details.

## 3-3. Fitting the Model

You can fit the model using `.fit()` method. When you didn't specify a `Trainer` in previous step, default settings would be used in the fitting. Else, you can specify `Trainer` implicitly by passing the trainer configurations as parameters for `.fit()`. 


> The training and valiation process is visualized in real-time using TensorBoard. 

## 3-4. Stacking Fitted Models

`Experiment` class has `.stack` as an attribute. If `.stack_models` is set to `True`, fitted models will automatically be saved to `.stack`. If `.stack_models` is set to `False`, it would stop stacking fitted models to the stack. However, it would still save the model that is just fitted i.e., it will have memory of 1 fit. You can toggle `.stack_models` using `.toggle_stack_models()` method.

Plus, you can check which model in the stack has the best performance using `.best_ckpt_in_stack()`.

## 3-5. Saving Models

You can save the current model using `.save_ckpt()` method, or you can save the models in the stack using `.save_stack()` method. After `.save_stack()`, `.stack` will be flushed.

## 3-6. Checking the Best Model Thus Far

With `.best_ckpt_thus_far()` method, you can check the best model saved (in local) thus far.

## 3-7. (Stratified) K-Fold Cross-Validation

You can perform (stratified) k-fold cross-validation using `.cross_validation()` method. See details in the [tutorial](https://colab.research.google.com/drive/1VZCR84K2pzKpZoFGy3kp8vOZYAYyvQjJ?usp=sharing).

> `.cross_validation()` is compatible with sci-kit learn models and their variants(e.g., xgboost) as well. Astrape is compatible with sci-kit learn models and pytorch-lightning modules.



