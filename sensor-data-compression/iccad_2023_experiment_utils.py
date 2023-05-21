import os
import time
import pickle
import codecs

def store_pefr_cifar10(i_fp_pefr, i_curr_bi, i_mispredicts, i_hess_trace, i_ce_loss):
    #S: Store start time
    time_s = time.time()

    #S: Create lists of new results to be stored
    lst_mispredicts = [i_mispredicts]
    lst_hess_trace  = [i_hess_trace]
    lst_ce_loss     = [i_ce_loss]

    #S: Load existing pickled results
    obj = None
    if os.path.exists(i_fp_pefr):
        pickled_obj = ""
        with open(i_fp_pefr, "r") as f:
            pickled_obj = f.read()
        obj = pickle.loads(codecs.decode(pickled_obj.encode(), "base64"))

    #S: Get dict object with bi_to_METRIC dictionaries
    if obj == None:
        obj = dict()
        obj["bi_to_mispredicts"] = dict()
        obj["bi_to_hess_trace"]  = dict()
        obj["bi_to_ce_loss"]     = dict()

    #S: Update bi_to_METRIC dictionaries with new results
    obj["bi_to_mispredicts"] [i_curr_bi] = lst_mispredicts
    obj["bi_to_hess_trace"]  [i_curr_bi] = lst_hess_trace
    obj["bi_to_ce_loss"]     [i_curr_bi] = lst_ce_loss

    #S: Pickle and store (updated) dict object
    pickled_obj = codecs.encode(pickle.dumps(obj), "base64").decode()
    with open(i_fp_pefr, "w") as f:
        f.write(pickled_obj)

    #S: Return elapsed time
    return time.time() - time_s

def store_pefr_econ_t(i_fp_pefr, i_curr_bi, i_hess_trace, i_ce_loss):
    #S: Store start time
    time_s = time.time()

    #S: Create lists of new results to be stored
    lst_hess_trace  = [i_hess_trace]
    lst_ce_loss     = [i_ce_loss]

    #S: Load existing pickled results
    obj = None
    if os.path.exists(i_fp_pefr):
        pickled_obj = ""
        with open(i_fp_pefr, "r") as f:
            pickled_obj = f.read()
        obj = pickle.loads(codecs.decode(pickled_obj.encode(), "base64"))

    #S: Get dict object with bi_to_METRIC dictionaries
    if obj == None:
        obj = dict()
        obj["bi_to_mispredicts"] = dict()
        obj["bi_to_hess_trace"]  = dict()
        obj["bi_to_ce_loss"]     = dict()

    #S: Update bi_to_METRIC dictionaries with new results
    obj["bi_to_hess_trace"]  [i_curr_bi] = lst_hess_trace
    obj["bi_to_ce_loss"]     [i_curr_bi] = lst_ce_loss

    #S: Pickle and store (updated) dict object
    pickled_obj = codecs.encode(pickle.dumps(obj), "base64").decode()
    with open(i_fp_pefr, "w") as f:
        f.write(pickled_obj)

    #S: Return elapsed time
    return time.time() - time_s

def store_pefd_experiment1(i_fp_pefd, i_curr_bi, i_loop_start, i_sub_times):
    #S: Store start time
    time_s = time.time()

    #S: Unpack times of subprocesses in FI loop
    dataset, gt_metric, ht_metric, pefr = i_sub_times

    #S: Create lists of new results to be stored
    lst_dataset   = [dataset]
    lst_gt_metric = [gt_metric]
    lst_ht_metric = [ht_metric]
    lst_pefr      = [pefr]
    lst_fi_loop   = [time.time() - i_loop_start]

    #S: Load existing pickled results
    obj = None
    if os.path.exists(i_fp_pefd):
        pickled_obj = ""
        with open(i_fp_pefd, "r") as f:
            pickled_obj = f.read()
        obj = pickle.loads(codecs.decode(pickled_obj.encode(), "base64"))

    #S: Get dict object with bi_to_METRIC dictionaries
    if obj == None:
        obj = dict()
        obj["bi_to_dataset"]   = dict()
        obj["bi_to_gt_metric"] = dict()
        obj["bi_to_ht_metric"] = dict()
        obj["bi_to_pefr"]      = dict()
        obj["bi_to_fi_loop"]   = dict()

    #S: Update bi_to_METRIC dictionaries with new results
    obj["bi_to_dataset"]   [i_curr_bi] = lst_dataset
    obj["bi_to_gt_metric"] [i_curr_bi] = lst_gt_metric
    obj["bi_to_ht_metric"] [i_curr_bi] = lst_ht_metric
    obj["bi_to_pefr"]      [i_curr_bi] = lst_pefr
    obj["bi_to_fi_loop"]   [i_curr_bi] = lst_fi_loop

    #S: Pickle and store (updated) dict object
    pickled_obj = codecs.encode(pickle.dumps(obj), "base64").decode()
    with open(i_fp_pefd, "w") as f:
        f.write(pickled_obj)

    #S: Return elapsed time
    return time.time() - time_s