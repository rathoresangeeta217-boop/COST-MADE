with open('src/lib/useFirestoreSync.ts', 'w') as f:
    f.write('''import { useEffect, useRef } from 'react';
import { useProjectStore } from '../store/useProjectStore';
import { useAuth } from './AuthContext';
import { db } from './firebase';
import { collection, doc, getDocs, query, writeBatch } from 'firebase/firestore';

export function useFirestoreSync() {
  const { user } = useAuth();
  const { projects } = useProjectStore();
  const isFirstLoad = useRef(true);

  // Load from Firestore
  useEffect(() => {
    async function loadProjects() {
      try {
        const q = query(collection(db, 'projects'));
        const snapshot = await getDocs(q);
        const fbProjects = snapshot.docs.map(doc => {
          const data = doc.data();
          return {
            id: data.id,
            name: data.name,
            clientName: data.clientName || '',
            createdAt: data.createdAt,
            updatedAt: data.updatedAt,
            items: data.items || []
          };
        });
        
        if (fbProjects.length > 0) {
          useProjectStore.setState(state => {
            const existingIds = new Set(fbProjects.map(p => p.id));
            const localOnly = state.projects.filter(p => !existingIds.has(p.id));
            return { projects: [...fbProjects, ...localOnly] };
          });
        }
      } catch (e) {
        console.error('Error loading projects:', e);
      }
      isFirstLoad.current = false;
    }
    
    loadProjects();
  }, []); // Run once on mount

  // Save to Firestore on change
  useEffect(() => {
    async function syncProjects() {
      if (!isFirstLoad.current) {
        try {
          const batch = writeBatch(db);
          for (const project of projects) {
            const docRef = doc(db, 'projects', project.id);
            batch.set(docRef, {
              ...project,
              userId: user?.uid || 'anonymous'
            }, { merge: true });
          }
          await batch.commit();
        } catch (e) {
          console.error('Error saving projects:', e);
        }
      }
    }
    
    syncProjects();
  }, [projects, user]);
}
''')
