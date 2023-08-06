# GradientAccumulator

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![CI](https://github.com/andreped/GradientAccumulator/workflows/CI/badge.svg)

This repo contains a TensorFlow 2 compatible implementation of accumulated gradients.

The proposed implementation simply overloads the train_step of a given tf.keras.Model, to update correctly according to a user-specified number of accumulation steps. This enables gradient accumulation, which reduces memory consumption and enables usage of theoretically infinitely large batch size (among other things), at the cost of increased training runtime.

Implementation is compatible with and have been tested against TF >= 2.2 and Python >= 3.6, and works cross-platform (Ubuntu, Windows, macOS).

## Install

Stable release:
```
pip install https://github.com/andreped/GradientAccumulator/releases/download/v0.1.2/GradientAccumulator-0.1.2-py3-none-any.whl
```

Or from source:
```
pip install git+https://github.com/andreped/GradientAccumulator
```

## Usage
```
from GradientAccumulator.GAModelWrapper import GAModelWrapper
from tensorflow.keras.models import Model

model = Model(...)
model = GAModelWrapper(n_gradients=4, inputs=model.input, outputs=model.output)
```

Then simply use the `model` as you normally would!

#### Mixed precision
There has also been added experimental support for mixed precision:
```
from tensorflow.keras import mixed_precision

mixed_precision.set_global_policy('mixed_float16')
model = GAModelWrapper(n_gradients=4, mixed_precision=True, inputs=model.input, outputs=model.output)
```

## Disclaimer
In theory, one should be able to get identical results for batch training and using gradient accumulation. However, in practice, one may observe a slight difference. One of the cause may be when operations are used (or layers/optimizer/etc) that update for each step, such as Batch Normalization. It is **not** recommended to use BN with GA, as BN would update too frequently. However, you could try to adjust the `momentum` of BN (see [here](https://keras.io/api/layers/normalization_layers/batch_normalization/)).

It was also observed a small difference when using adaptive optimizers, which I believe might be due to how frequently they are updated. Nonetheless, for the optimizers, the difference was quite small, and one may approximate batch training quite well using our GA implementation, as rigorously tested [here](https://github.com/andreped/GradientAccumulator/tree/main/tests)).

## TODOs:
- [x] Add generic wrapper class for adding accumulated gradients to any optimizer
- [x] Add CI to build wheel and test that it works across different python versions, TF versions, and operating systems.
- [x] Add benchmarks to verfiy that accumulated gradients actually work as intended
- [x] Add class_weight support
- [x] GAModelWrapper gets expected identical results to batch training!
- [x] Test method for memory leaks
- [x] Add multi-input/-output architecture support
- [x] Add mixed precision support
- [ ] Add wrapper class for BatchNormalization layer, similar as done for optimizers
- [ ] Add proper multi-GPU support

## Acknowledgements
This implementation is based on the implementation presented in [this thread](https://stackoverflow.com/a/66524901) on stack overflow.

This repository serves as an open solution for everyone to use, until TF/Keras integrates a proper solution into their framework(s).

## Troubleshooting
Overloading of `train_step` method of tf.keras.Model was introduced in TF 2.2, hence, this code is compatible with TF >= 2.2.

Also, note that TF depends on different python versions. If you are having problems getting TF working, try a different TF version or python version.

For TF 1, I suggest using the AccumOptimizer implementation in the [H2G-Net repository](https://github.com/andreped/H2G-Net/blob/main/src/utils/accum_optimizers.py#L139) instead, which wraps the optimizer instead of overloading the train_step of the Model itself (new feature in TF2).
