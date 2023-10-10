import os
from time import sleep
from poeditor import POEditorAPI 

API_TOKEN = os.environ.get('API_TOKEN')
SOURCE_PROJECT = os.environ.get('SRC_ID')
DEST_PROJECT = os.environ.get('DST_ID')

dsttermlist = list()
newterms = list()
newlangs = list()

doit = True

if API_TOKEN is None:
    raise AssertionError
if SOURCE_PROJECT is None:
    raise AssertionError
if DEST_PROJECT is None:
    raise AssertionError

client = POEditorAPI(api_token=API_TOKEN)

srcprj = client.view_project_details(project_id=SOURCE_PROJECT)
dstprj = client.view_project_details(project_id=DEST_PROJECT)

# Make sure all terms from source project are in up-to-date in dest project
srcterms = client.view_project_terms(project_id=srcprj['id'])
dstterms = client.view_project_terms(project_id=dstprj['id'])

dsttermlist = [ x['term'] for x in dstterms]

print(f'Source has {len(srcterms)} terms, destination has {len(dstterms)} terms.')
for term in srcterms:
    if term['term'] not in dsttermlist:
        print(f'Found new destination term {term["term"]}')
        newterms.append(term)

if newterms:
#    client.add_terms(project_id=dstprj['id'], data=newterms)
    print(f'Would add terms: {newterms}')

# Sync languages
srclangs = client.list_project_languages(project_id=srcprj['id'])
dstlangs = client.list_project_languages(project_id=dstprj['id'])

dstlanglist = [ x['code'] for x in dstlangs]

for lang in srclangs:

   if lang['code'] not in dstlanglist:
     newlangs.append(lang['code'])

if newlangs:
    print(f'Would add languages: {newlangs}')

    if doit:
        for lang in newlangs:
            print(f'Adding language {lang}')
            client.add_language_to_project(project_id=dstprj['id'], language_code=lang)

else:
    print('No new languages to sync from source to destination')

# Sync translations for all languages in destination

if newlangs:
    dstlangs = client.list_project_languages(project_id=dstprj['id'])

for lang in dstlangs:
    if lang['code'] == dstprj['reference_language']:
        print(f'Reference language {lang["code"]} detected. Skipping download!')
    else:

      file_url, local_file = client.export(project_id=srcprj['id'], language_code=lang['code'], file_type='json')
      print(f'Got details for {lang["code"]} in {local_file}')

      if doit:
        print(f'Updating {lang["code"]}')
        client.update_translations(project_id=dstprj['id'], file_path=local_file, language_code=lang['code'])
        print('Sleeping 20s to avoid API limits')
        sleep(20)

# Sync contributors


