### Finding scrapes in folders

```
    # return dirs
    # for dir in dirs:
    #     if dir in ('.ipynb_checkpoints', '_other'):
    #         continue
    #     if dir == 'combined':
    #         combined_dirs = os.listdir('combined')
    #         for comb in combined_dirs:
    #             for file in comb:
    #                 if file.endswith('.csv'):
    #                     result = date_regex.search(file)
    #                     term = result.group(1)
    #                     date = result.group(2)
    #                     dir_objs.append(
    #                         {
    #                             term: term,
    #                             date: date
    #                         }
    #                     )
    #     else:
    #         term_dirs = os.listdir(dir)
    #         for folder in term_dirs:
    #             if folder == '.ipynb_checkbpoints':
    #                 continue
    #             for subfolder in folder:
    #                 if file.endswith('.csv'):
```

Used instead: os.walk

### Print a dataframe into HTML

```
    # basic rendering

    # return render_template('plots/dataframe_basic.html',
    #     tables=[result_df.head().to_html(classes='data')],
    #     titles=result_df.columns.values,
    #     result_shape = result_shape)

    # prettier rendering

    # return render_template("plots/dataframe_extra.html",
    #         column_names=result_df.columns.values,
    #         row_data=list(result_df.head().values.tolist()),
    #         link_column="title", zip=zip,
    #         result_shape=result_shape)
```

### Combine scrap and api results - moved to a separate function
```
# or get results from existing ones
# else:
#     os.chdir(exists_path)
#     all_path = exists_path + '/' + 'all'
#     # check if a combined file exists
#     if os.path.exists(all_path):
#         os.chdir(all_path)
#         files = os.listdir()
#         for file in files:
#             if file.endswith('.csv'):
#                 result_df = pd.read_csv(file, index_col=0)
#     # combine files
#     else:
#         # get the files
#         paths = [
#             'combined',
#             'fluff'
#         ]
#         for folder_path in paths:    
#             try:
#                 os.chdir(folder_path)
#                 combined_paths = os.listdir()
#                 for c_path in combined_paths:
#                     if c_path.endswith(".csv"):
#                         combined_df = pd.read_csv(c_path, index_col = 0)
#                         result_df = pd.concat([result_df, combined_df])
#             except:
#                 pass
#             os.chdir('..')
        
#         os.chdir('..')
#     result_shape = result_df.shape
```