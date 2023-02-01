import numpy as np

def normalize(data, sumlog2=True):
    """
    Normalize data by dividing by the sum of the log2 of the occupancy
    """
    maxes = []
    sums = []
    sums_log2 = []
    for i in range(len(data)):
        maxes.append(data[i].max())
        sums.append(data[i].sum())
        sums_log2.append(2 ** (np.floor(np.log2(data[i].sum()))))
        if sumlog2:
            data[i] = 1.0 * data[i] / (sums_log2[-1] if sums_log2[-1] else 1.0)
        else:
            data[i] = 1.0 * data[i] / (data[i].sum() if data[i].sum() else 1.0)
    sums_arr = np.array(sums_log2) if sumlog2 else np.array(sums)
    return (
        data,
        np.array(maxes),
        sums_arr,
    )

def unnormalize(norm_data, max_vals, sumlog2=True):
    for i in range(len(norm_data)):
        if sumlog2:
            sumlog2 = 2 ** (np.floor(np.log2(norm_data[i].sum())))
            norm_data[i] = (
                norm_data[i] * max_vals[i] / (sumlog2 if sumlog2 else 1.0)
            )
        else:
            norm_data[i] = (
                norm_data[i]
                * max_vals[i]
                / (norm_data[i].sum() if norm_data[i].sum() else 1.0)
            )
    return norm_data