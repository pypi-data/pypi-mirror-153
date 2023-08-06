// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
/// @file
/// @author Simon Heybrock
#pragma once

#include "scipp-variable_export.h"
#include "scipp/variable/variable.h"

/* #undef GENERATE_OUT */

namespace scipp::variable {

[[nodiscard]] SCIPP_VARIABLE_EXPORT Variable greater(const Variable &a, const Variable &b);
#ifdef GENERATE_OUT
SCIPP_VARIABLE_EXPORT Variable &greater(const Variable &a, const Variable &b, Variable &out);
#endif
} // namespace scipp::variable
