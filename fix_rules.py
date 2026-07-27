with open('firestore.rules', 'w') as f:
    f.write('''rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /projects/{projectId} {
      allow read, write: if true;
    }
  }
}''')
