// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
/// @file
/// @author Jan-Lukas Wynen
#pragma once

#include "scipp/dataset/dataset.h"

namespace scipp::dataset {

[[nodiscard]] SCIPP_DATASET_EXPORT DataArray
all(const DataArray &a);

[[nodiscard]] SCIPP_DATASET_EXPORT DataArray
all(const DataArray &a, Dim dim);

[[nodiscard]] SCIPP_DATASET_EXPORT Dataset
all(const Dataset &d);

[[nodiscard]] SCIPP_DATASET_EXPORT Dataset
all(const Dataset &d, Dim dim);

} // namespace scipp::dataset
