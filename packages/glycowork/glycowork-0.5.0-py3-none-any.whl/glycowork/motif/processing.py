import pandas as pd
import numpy as np
import random
from glycowork.glycan_data.loader import unwrap, linkages

def small_motif_find(glycan):
  """processes IUPACcondensed glycan sequence (string) without splitting it into glycowords\n
  | Arguments:
  | :-
  | glycan (string): glycan in IUPAC-condensed format\n
  | Returns:
  | :-
  | Returns string in which glycoletters are separated by asterisks
  """
  b = glycan.replace('[', '').replace(']', '').replace(')', '(').split('(')
  return '*'.join(b)

def min_process_glycans(glycan_list):
  """converts list of glycans into a nested lists of glycoletters\n
  | Arguments:
  | :-
  | glycan_list (list): list of glycans in IUPAC-condensed format as strings\n
  | Returns:
  | :-
  | Returns list of glycoletter lists
  """
  glycan_motifs = [small_motif_find(k) for k in glycan_list]
  glycan_motifs = [i.split('*') for i in glycan_motifs]
  return glycan_motifs

def get_lib(glycan_list):
  """returns sorted list of unique glycoletters in list of glycans\n
  | Arguments:
  | :-
  | glycan_list (list): list of IUPAC-condensed glycan sequences as strings\n
  | Returns:
  | :-
  | Returns sorted list of unique glycoletters (strings) in glycan_list
  """
  #convert to glycoletters
  proc = min_process_glycans(glycan_list)
  #flatten nested lists
  lib = unwrap(proc)
  #get unique vocab
  lib = list(sorted(list(set(lib))))
  return lib

def expand_lib(libr, glycan_list):
  """updates libr with newly introduced glycoletters\n
  | Arguments:
  | :-
  | libr (list): sorted list of unique glycoletters observed in the glycans of our dataset
  | glycan_list (list): list of IUPAC-condensed glycan sequences as strings\n
  | Returns:
  | :-
  | Returns new lib
  """
  new_lib = get_lib(glycan_list)
  return list(sorted(list(set(libr + new_lib))))

def seed_wildcard(df, wildcard_list, wildcard_name, r = 0.1, col = 'target'):
  """adds dataframe rows in which glycan parts have been replaced with the appropriate wildcards\n
  | Arguments:
  | :-
  | df (dataframe): dataframe in which the glycan column is called "target" and is the first column
  | wildcard_list (list): list which glycoletters a wildcard encompasses
  | wildcard_name (string): how the wildcard should be named in the IUPAC-condensed nomenclature
  | r (float): rate of replacement, default is 0.1 or 10%
  | col (string): column name for glycan sequences; default: target\n
  | Returns:
  | :-
  | Returns dataframe in which some glycoletters (from wildcard_list) have been replaced with wildcard_name
  """
  ###this function probably will be deprecated at some point
  added_rows = []
  #randomly choose glycans and replace glycoletters with wildcards
  for k in range(len(df)):
    temp = df[col].values.tolist()[k]
    for j in wildcard_list:
      if j in temp:
        if random.uniform(0, 1) < r:
          added_rows.append([temp.replace(j, wildcard_name)] + df.iloc[k, 1:].values.tolist())
  added_rows = pd.DataFrame(added_rows, columns = df.columns.values.tolist())
  #append wildcard-modified glycans and their labels to original dataframe
  df_out = pd.concat([df, added_rows], axis = 0, ignore_index = True)
  return df_out

def presence_to_matrix(df, glycan_col_name = 'target', label_col_name = 'Species'):
  """converts a dataframe such as df_species to absence/presence matrix\n
  | Arguments:
  | :-
  | df (dataframe): dataframe with glycan occurrence, rows are glycan-label pairs
  | glycan_col_name (string): column name under which glycans are stored; default:target
  | label_col_name (string): column name under which labels are stored; default:Species\n
  | Returns:
  | :-
  | Returns pandas dataframe with labels as rows and glycan occurrences as columns
  """
  glycans = list(sorted(list(set(df[glycan_col_name].values.tolist()))))
  species = list(sorted(list(set(df[label_col_name].values.tolist()))))
  #get a count matrix for each rank - glycan combination
  mat_dic = {k:[df[df[label_col_name] == j][glycan_col_name].values.tolist().count(k) for j in species] for k in glycans}
  mat = pd.DataFrame(mat_dic)
  mat.index = species
  return mat

def choose_correct_isoform(glycans, reverse = False):
  """given a list of glycan branch isomers, this function returns the correct isomer\n
  | Arguments:
  | :-
  | glycans (list): glycans in IUPAC-condensed nomenclature
  | reverse (bool): whether to return the correct isomer (False) or everything except the correct isomer (True); default:False\n
  | Returns:
  | :-
  | Returns the correct isomer as a string (if reverse=False, otherwise it returns a list of strings)
  """
  #get what is before the first branch & its length for each glycan
  prefix = min_process_glycans([glyc[:glyc.index('[')] for glyc in glycans])
  prefix_len = [len(k) for k in prefix]
  #choose the isoform with the longest main chain before the branch & or the branch ending in the smallest number if all lengths are equal
  if len(set(prefix_len)) == 1:
    branch_endings = [int(k[-2][-1]) if k[-2][-1] != 'z' and k[-2][-1] != 'd' else 10 for k in prefix]
    correct_isoform = glycans[np.argmin(branch_endings)]
  else:
    correct_isoform = glycans[np.argmax(prefix_len)]
  if reverse:
    glycans.remove(correct_isoform)
    correct_isoform = glycans
  return correct_isoform
