# FindingDuplicateFiles

Run the code using command: python findingDuplicateFiles.py <directoryName>

Project description: A directory structure contains 100G size of files. The
                     depth, number of sub-directories and files is not known, nor the file size.
                     Soft-links and hard-links can also be expected. Write a program that traverses the
                     whole structure efficiently and clusters  duplicate files. 
                     Two files are considered as duplicates when they have the same content.

Solution overview: Files are first clustered based on their sizes. Two files with the same size
                   will be in the same cluster. Clusters that contains only one file are filtered out.
                   Files are re clustered using the md5 hash of their content. This time, two files
                   will be in the same cluster only if their content is same. 
                   Since the number of files is huge (their size can be huge too), I first cluster 
                   based file size and reduce the number of candidate clusters by filtering out
                   single element list.

