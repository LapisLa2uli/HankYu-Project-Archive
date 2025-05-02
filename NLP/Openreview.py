import openreview, csv, os

'''# Fetching all venues V1
client = openreview.Client(baseurl='https://api.openreview.net')  # ,
#                            username='<your username>',
#                            password='<your password>')
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net'
)
venue_group = client.get_group('ICLR.cc/2020/Conference')
submission_name = venue_group.content['submission_name']['value']
submissions = client.get_all_notes(invitation=f'ICLR.cc/2020/Conference/-/{submission_name}')'''
invitation = "ICLR.cc/2017/conference/-/submission"
'''submissions = client.get_all_notes(
    invitation=invitation,details='directReplies')
print(submissions[0])
venues = client.get_group(id='venues').members
print(venues)
f=open('submissions.txt','w',encoding='utf-8')
f.write(str(submissions))
f.close()
reviews = []
for submission in submissions:
    reviews = reviews + [openreview.Note.from_json(reply) for reply in submission.details["directReplies"] if
                         reply["invitation"].endswith("Official_Review")]

invitation = client.get_invitation("NeurIPS.cc/2022/Conference/-/Blind_Submission")
keylist = list(review_invitation.reply['content'].keys())
with open('reviews.csv', 'w') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    # Write header
    t = csvwriter.writerow(keylist)
    for review in reviews:
        valueList = []
        for key in keylist:
            if review.content.get(key):
                if 'value' in review.content[key].keys():
                    valueList.append(review.content.get(key)['value'])
                else:
                    valueList.append(review.content.get(key))
            else:
                valueList.append('')
        s = csvwriter.writerow(valueList)
outfile.close()
# Fetching all venues V2
client = openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net')
venue_id = 'ICLR.cc/2017/conference'
venue_group = client.get_group(venue_id)
print(venue_group.content)

submission_name = venue_group.content['submission_name']['value']
submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')
review_name = venue_group.content['review_name']['value']

reviews=[openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies']
         if f'{venue_id}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']]
f = open('submissions.txt', 'w')
f.write(str(submissions))
f.close()
# f=open('reviews.txt','w')
# f.write(reviews)
# f.close()
'''


os.chdir('D://stuff//NLP//2017 Papers//PDF')
client = openreview.Client(baseurl='https://api.openreview.net')
venues = client.get_group(id='venues').members
print(venues)
# Step 2: Retrieve all submissions
notes = client.get_all_notes(invitation=invitation)
print(notes)
'''# Step 3: Download PDFs
for note in notes:
    try:
        print(note.id)
        f = client.get_attachment(note.id, 'pdf')
        print(f'writing {note.id}.pdf')
        with open(f'{note.id}.pdf', 'wb') as op:
            op.write(f)
            op.close()
    except:
        print(f'ERROR: {note.id}.pdf')

# Optional: Download supplementary materials
for note in notes:
    if note.content.get("supplementary_material", {}).get('value'):
        f = client.get_attachment(note.id, 'supplementary_material')
        with open(f'submission{note.id}_supplementary_material.zip', 'wb') as op:
            op.write(f)'''