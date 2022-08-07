import { serverTimestamp } from 'firebase/database';

export class Collection {
    id: string = '';
    name: string = '';
    image: string = '';
    note: string = '';
    createdAt: any = serverTimestamp();
    modifiedAt: any = Date.now();
    isDeleted: boolean;
}
