/**
	String Similarity Algo
**/	

import java.util.PriorityQueue;
import uk.ac.shef.wit.simmetrics.similaritymetrics.JaroWinkler;

public class StringSimilarity{
	public int edit_distance(String ontology, String keyword){
		int [][] opt = new int [ontology.length()+1][keyword.length()+1];
		// init
		for (int i=0; i<opt.length; i++){
			opt[i][0] = i;
		}
		for (int j=0; j<opt[0].length; j++){
			opt[0][j] = j;
		}
	
		// calculate optimal values
		for (int i=1; i<opt.length; i++){
			for(int j=1; j<opt[0].length; j++){
				if(keyword.charAt(j-1) != ontology.charAt(i-1)){
					opt[i][j] = min(1+opt[i-1][j], 1+opt[i][j-1], 1+opt[i-1][j-1]);
				}
				else {
					opt[i][j] = opt[i-1][j-1];
				}
			}
		}
		return opt[opt.length-1][opt[0].length-1];
	}

	public String most_common_substring(String ontology, String keyword){
		int [][] opt = new int [ontology.length()+1][keyword.length()+1];
		String max_str = "";
		int max_len_so_far = 0;
		
		for (int i=0; i<opt.length-1; i++){
			for(int j=0; j<opt[0].length-1; j++){
				if (keyword.charAt(j) == ontology.charAt(i)){
					opt[i+1][j+1] = opt[i][j]+1;
					if (opt[i+1][j+1] > max_len_so_far){
						max_len_so_far = opt[i+1][j+1];
						max_str = ontology.substring(i-max_len_so_far+1, i+1);
					}
				}
			}
		}
		return max_str;
	}


	private int min(int... ele){
		PriorityQueue<Integer> queue = new PriorityQueue<Integer>();
		for(int e : ele){
			queue.add(e);
		}		
		return queue.poll();
	}


	public double compareString(String ontology, String keyword){
		JaroWinkler algo = new JaroWinkler();
		return algo.getSimilarity(ontology, keyword);
	}


	public static void main(String [] args){
		StringSimilarity ss = new StringSimilarity();
		System.out.println(ss.compareString(args[0].trim().toLowerCase(), args[1].trim().toLowerCase()));
	}
}
