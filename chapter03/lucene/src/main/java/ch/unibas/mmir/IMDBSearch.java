package ch.unibas.mmir;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.FilteringTokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.en.EnglishPossessiveFilter;
import org.apache.lucene.analysis.en.KStemFilter;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

public class IMDBSearch {

    // loading IMDB documents
    // ----------------------------------------------------------------------------------------
    public static ArrayList<Map<String, String>> read_collection(String name) throws IOException {
        ArrayList<Map<String, String>> docs = new ArrayList<Map<String, String>>();
        String splitter = ",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)";
        BufferedReader reader = new BufferedReader(new FileReader(name));
        String line, keys[] = reader.readLine().split(splitter);

        while ((line = reader.readLine()) != null) {
            String[] values = line.split(splitter);
            Map<String, String> dataMap = new HashMap<>();

            for (int i = 0; i < keys.length; i++) {
                // dataMap.put(keys[i], values[i]);
                switch (keys[i]) {
                    case "Series_Title":
                        dataMap.put("title", values[i]);
                        break;
                    case "Released_Year":
                        dataMap.put("year", values[i]);
                        break;
                    case "Runtime":
                        dataMap.put("runtime", values[i].replace(" min", ""));
                        break;
                    case "Genre":
                        dataMap.put("genre", values[i].replace(",", ""));
                        break;
                    case "IMDB_Rating":
                        dataMap.put("rating", values[i]);
                        break;
                    case "Overview":
                        dataMap.put("summary", values[i]);
                        break;
                    case "Star1":
                        dataMap.put("actors", values[i]);
                        break;
                    case "Star2":
                    case "Star3":
                    case "Star4":
                        dataMap.put("actors", dataMap.get("actors") + " " + values[i]);
                        break;
                }
            }
            docs.add(dataMap);
        }
        reader.close();

        // print summary
        System.out.println("Read " + docs.size() + " documents from " + name);
        return docs;
    }

    // analyzer demo
    // ----------------------------------------------------------------------------------------

    public static class MyAnalyzer extends Analyzer {
        @Override
        protected TokenStreamComponents createComponents(String fieldName) {
            final Tokenizer source = new StandardTokenizer();
            TokenStream result = new EnglishPossessiveFilter(source);
            // result = new LowerCaseFilter(result);
            result = new FilteringTokenFilter(result) {
                private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);

                @Override
                protected boolean accept() throws IOException {
                    return termAtt.length() > 3;
                }
            };
            result = new KStemFilter(result);
            return new TokenStreamComponents(source, result);
        }
    }

    public static void print_tokens(Analyzer analyzer, String text) throws IOException {
        TokenStream ts = analyzer.tokenStream("text", new StringReader(text));
        CharTermAttribute termAtt = ts.addAttribute(CharTermAttribute.class);

        for (ts.reset(); ts.incrementToken();)
            System.out.print(termAtt.toString() + " ");
        ts.end();
        System.out.println();
    }

    public static void run_analyzer_example() throws IOException {
        String text = "I think text's values' color goes here; WHAT happens with it? do we see IT again; I went there to be gone with houses";
        CharArraySet stopWords = new CharArraySet(Arrays.asList("i", "do"), true);

        System.out.println("             text: " + text);
        System.out.println();

        // standard analyzer
        System.out.print("         standard: ");
        print_tokens(new StandardAnalyzer(), text);

        // english analyzer (with porter stemmer)
        System.out.print("          english: ");
        print_tokens(new EnglishAnalyzer(), text);

        // english analyzer (with porter stemmer) and new set of stopwords
        System.out.print("english/stopwords: ");
        print_tokens(new EnglishAnalyzer(stopWords), text);

        // a custom analyzer, no lower case and kstemmer
        System.out.print("      my analyzer: ");
        print_tokens(new MyAnalyzer(), text);
    }

    // main function and demo dispatcher
    // ----------------------------------------------------------------------------------------

    public static void main(String[] args) throws IOException {
        // check on arguments and run parts of demo
        String action = args.length > 0 ? args[0].toLowerCase() : "analyze";

        // if action starts with "ana", run analyzer example
        if (action.startsWith("ana")) {
            System.out.println("IMDBSearch: running analyzer example");
            System.out.println();
            run_analyzer_example();
        } else
            System.out.println("IMDBSearch: unknown action `" + action + "`");
        System.out.println();
    }
}