from get_s3_paths import get_subs
import os
import numpy as np
import pandas
import patsy
from CPAC.utils import create_fsl_model as cfsl
from patsy import missing
import types

# ## Handle NAs in csv to pass through instead of drop
# def new_handle_NA(self, values, is_NAs, origins):
#     assert len(values) == len(is_NAs) == len(origins)
#     if len(values) ==0:
#         return values
#     if self.on_NA == 'na':
#         for is_NA in is_NAs:
            
        
# missing._valid_NA_responses = ['drop','raise','na']
# na = missing.NAAction()
# na.on_NA = 'na'
# na.handle_NA = types.MethodType(new_handle_NA, na)

def greater_than(dmat, a, b):
    c1 = positive(dmat, a)
    c2 = positive(dmat, b)
    return c1-c2

def positive(dmat, a):
    evs = dmat.design_info.column_name_indexes
    con = np.zeros(dmat.shape[1])
    if a in evs:
        con[evs[a]] = 1
    else:
        #it is a dropped term so make all other terms in that category at -1
        term = a.split('[')[0]
        for ev in evs:
            if ev.startswith(term):
                con[evs[ev]]= -1
    con[0] = 1
    return con

def negative(dmat, a):
    con = 0-positive(dmat, a)
    return con

def create_dummy_string(length):
    ppstring = ""
    for i in range(0, length):
        ppstring += '\t' + '%1.5e' %(1.0)
    ppstring += '\n' 
    return ppstring

def create_con_file(con_dict, file_name, out_dir):
    with open(os.path.join(out_dir, file_name)+".con",'w+') as f:
        #write header
        for key in con_dict:
            f.write("/ContrastName1\t\"%s\"\n" %key)
        f.write("/NumWaves\t%d\n" %len(con_dict[key]))
        f.write("/NumContrasts\t%d\n" %len(con_dict))
        f.write("/PPString%s" %create_dummy_string(len(con_dict[key])))
        f.write("/RequiredEffect%s" %create_dummy_string(len(con_dict[key])))
        f.write("\n\n")

        #write data
        f.write("/Matrix\n")
        for key in con_dict:
            for v in con_dict[key]:
                f.write("%1.5e\t" %v)
            f.write("\n")
    return os.path.join(out_dir, file_name)

model_name = "ABIDE_dx_age_site_fiq_meanfd"

#load phenotypic data
csv_path = 'Phenotypic_V1_0b_preprocessed1.csv'
csv_in = pandas.read_csv(csv_path)

#get relevant subjects
sub_pheno_list = get_subs(csv_in)
extract = [f in sub_pheno_list for f in csv_in['FILE_ID']]
data_subset = csv_in.ix[extract,:]

#construct design matrix (model file)
dmat = patsy.dmatrix("C(DX_GROUP, Sum) + AGE_AT_SCAN + C(SITE_ID, Sum) + FIQ + func_mean_fd", data_subset, NA_action="raise")
dm = np.asarray((dmat))

#make contrasts
#baseline is called "Intercept"
contrasts = dict()
#contrasts["TDCgtASD"] = greater_than(dmat, "Intercept", "C(DX_GROUP, Sum)[T.2]")
contrasts["ASDgtTDC"] = greater_than(dmat, "C(DX_GROUP, Sum)[S.1]", "C(DX_GROUP, Sum)[S.2]")
contrasts["TDCgtASD"] = greater_than(dmat, "C(DX_GROUP, Sum)[S.2]","C(DX_GROUP, Sum)[S.1]")

#output model, group, contrast, & ftst files
cfsl.create_mat_file(dm, model_name, '.')
cfsl.create_grp_file(dm, model_name, None, '.')
con_file = create_con_file(contrasts, model_name, '.')
#cfsl.create_con_ftst_file(con_file, model_name, None, '.')
