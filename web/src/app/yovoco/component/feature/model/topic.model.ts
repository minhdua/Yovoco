import { Timestamp, DocumentReference } from '@firebase/firestore';

export class Topic {
    id: string;
    name: string;
    collectionId: DocumentReference;
    index: number;
    image: string;
    note: string;
    createdAt: Timestamp;
    modifiedAt: Timestamp;
    isDeleted: boolean;
}
