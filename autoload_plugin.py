# -*- coding: utf-8 -*-

# Copyright ©2018 Jason Beach and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



import os
from os.path import isfile, join

import re
import sys
import json
import pandas as pd

from nikola import utils
from nikola.plugin_categories import Command
from nikola.plugins.command import new_post

LOGGER = utils.get_logger('AutoLoader', utils.STDERR_HANDLER)

"""
dir_path = './test/post_files/'
csv_path = './test/filesMeta.csv'
"""


class CommandAutoLoader(Command):
    """Automatically load many posts to blog"""

    name = "autoloader"
    needs_config = True
    doc_usage = ""
    doc_purpose = "load many posts at once"

    def _execute(self, dir_path, csv_path):
        """Automatically load many posts to blog"""
        # check args
        if not os.path.exists(dir_path):
            LOGGER.error('File directory does not exist')
            sys.exit()
        if not os.path.exists(csv_path):
            LOGGER.error('Metadata file does not exist')
            sys.exit()


        # get ipynb files from directory
        only_files = [f for f in os.listdir(dir_path) if isfile(join(dir_path, f))]
        file_path = [join(dir_path, f) for f in only_files]


        # check for teaser html-comment requirement
        tag = '<!-- TEASER_END -->'
            #tag = '(yo mama)'
        pattern = re.compile(tag)
        files_without_teaser = []

        for file in file_path:
            with open(file,'r') as txt_wrapper:
                content=txt_wrapper.read().replace('\n','')
                if not re.search(pattern, content):
                    files_without_teaser.append(file)
                
        if len(files_without_teaser) > 0:
            for file in files_without_teaser:
                print('No teaser found for file:', file)
            sys.exit()


        # prepare dataframes
        d = { 'file_path':pd.Series(file_path), 'file_name':pd.Series(only_files) }
        dfOnlyFiles = pd.DataFrame(d)

        dfMetaData = pd.read_csv(csv_path)
        dfFileData = dfMetaData.merge(dfOnlyFiles, how='inner', on='file_name')

        dfTmp = dfMetaData.merge(dfOnlyFiles, how='left', on='file_name')
        dfMissing = dfTmp[dfTmp['file_path'].isnull()]
        lMissing = dfMissing['file_name'].tolist()
        if len(lMissing)>0:
            print('The following files are in the .csv, but not found in the directory:',lMissing)


        # cmd new_post for each file
        N = dfFileData.shape[0]
        for i in range(0,N-1):
            df = dfFileData.iloc[i]
            lOps = ['--format=',df['format'],' --import=',df['file_path'],' title=',df['title'],' --tags=',df['tags']]     
            sOps = ''.join(lOps)
            lArgs= ['posts/',df['category'],'/']
            sArgs= ''.join(lArgs)
            #obj = new_post.CommandNewPost()
            #obj._execute(options=sOps,args=sArgs)

            os.system('nikola new_post '+sOps+sArgs)
            fChgPostMeta(post_path, category)


        # change posted files' metadata to include category

        #test
        #os.chdir('/home/jason/Desktop/WORKING/rprt_Ipynb/IMTorgDemo.github.io')
        #post_path = './posts/jupyter/display-system.ipynb'
        #category = 'cat-1'
        #future: change date, also

        def fChgPostMeta(post_path, category):
            with open(post_path,'r+') as txt_wrapper:
                jsondoc = json.load(txt_wrapper)
                jsondoc['metadata']['nikola']['category'] = category
            with open(post_path,'w') as txt_wrapper:
                txt_wrapper.write( json.dumps(jsondoc) )


        






