# Team 2 Capstone Setup

#### Create a Cloud Storage Bucket
 
```gsutil mb gs://$GOOGLE_CLOUD_PROJECT``` 

#### Copy project data files

```gsutil -m cp -r gs://cloud-training/specialized-training/dsl_data/* gs://$GOOGLE_CLOUD_PROJECT```

Added the `-m` option based on this feedback and it was significantly faster
```
==> NOTE: You are performing a sequence of gsutil operations that may
run significantly faster if you instead use gsutil -m cp ... Please
see the -m section under "gsutil help options" for further information
about when gsutil -m can be advantageous.
```
#### Setup Cloud Shell Python Virtual env

```
python -m venv .venv
source .venv/bin/activate
pip install google-cloud google.auth google-cloud-bigquery
```