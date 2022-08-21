import { Injectable } from '@angular/core';
import { TreeNode } from 'primeng/api';
@Injectable({
	providedIn: 'root',
})
export class TreeNodeService {
	constructor() {}

	flattern(nodes: TreeNode<any>[]) {
		let flatterned: TreeNode<any>[] = [];
		nodes.forEach(node => {
			flatterned.push(node);
			if (node.children) {
				flatterned = flatterned.concat(this.flattern(node.children));
			}
		});
		return flatterned;
	}
}
