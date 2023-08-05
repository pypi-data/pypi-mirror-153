## Part 3 - Project testing - predict dataset {#quick_start3}

To test our project we will need to run the model on a dataset, there are basically two main entry 
points to the pipeline that we can use for local testing, in this document we will cover one:

&nbsp;
### Using the pipeline_test.py

The **pipeline_test.py** initially it looks like this:
```
if __name__ == '__main__':
    p = <my-new-project>Pipeline()    
    output = p.execute()
    print("results: ", output)
```

Load the dataset for testing and pass it via the execute method, use the variable names declared in the <my-new-project>Inputs class, 
as in the following examples:
```
if __name__ == '__main__':
    p = <my-new-project>Pipeline() 
    with open('./example.html', 'r', encoding="utf8") as file:
        data = file.read()        
        output = p.execute(html_content=data, source='', title='', queue_name='')
        print("results: ", output)
```
or
```
if __name__ == '__main__':
    p = <my-new-project>Pipeline() 
    data_files = ['Utils/email_sample.json']
    data = {}
    for file in data_files:
        with open(file) as f:
            data = load_json(f)
    
    output = p.execute(**data)
    print("results: ", output)
```
or
```
if __name__ == '__main__':
    p = <my-new-project>Pipeline()
    
    df_in.url = 'http://apple.com/leadership'
    df_in.helper_url_list = ['http://apple.com/']
    output = p.execute(url=df_in.url, helper_url_list=df_in.helper_url_list)
    print("results: ", output)
```

Run **pipeline_test.py** and see the results.

