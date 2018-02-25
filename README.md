

# References
[use: new_post](https://github.com/getnikola/nikola/blob/master/nikola/plugins/command/new_post.py#L217)
[ex: plugin](https://github.com/getnikola/nikola/blob/master/nikola/plugins/command/plugin.py)
[doc: extension](https://getnikola.com/extending.html)
[doc: plugin repos](https://github.com/getnikola/plugins)


# Dependencies

* directory of .ipynb files
* .csv metadata file 

.csv file should contain:

* file name
* title
* format
* category
* tags



# Logic

- import metadata file
- create strings:
  + ipynb file path string for each file
  + options / args
  + nikola new_post --format=ipynb --import=./prebuild/tests/Display\ System.ipynb --title=Display\ System --tags=test_tag-1,test_tag-2 posts/test_category/

- check for `<!-- TEASER_END -->`

- loop through each file
  + create post
  + change post_file metadata to add category
- record errors
- output results / errors



# Learn

- run plugin
- nikola NewPost command




