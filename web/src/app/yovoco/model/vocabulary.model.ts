import { Timestamp, DocumentReference } from '@firebase/firestore';

export class Topic {
    id: string;
    topicId: DocumentReference;
    wordId: DocumentReference;
    index: number;
    phonetic: string;
    pos: string;
    definition: string;
    meaning: string;
    example: string[];
    synonym: string[];
    antonym: string[];
    stem: string;
    voices: string[];
    image: string[];
    note: string;
    createdAt: Timestamp;
    modifiedAt: Timestamp;
    isDeleted: boolean;
}
