package ch.unibas.mmir;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.StringReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.List;

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
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.document.IntField;
import org.apache.lucene.document.FloatField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class IMDBSearch {

    private static final String fileImdbDataset = "../datasets/imdb_top_1000.csv";
    private static final String pathIndex = "./index";

    // loading IMDB documents
    // ----------------------------------------------------------------------------------------
    public static List<Map<String, String>> readCollection(String name) throws IOException {
        List<Map<String, String>> docs = new ArrayList<Map<String, String>>();
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
                        dataMap.put("summary", values[i].replace("\"", ""));
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

    static public void showImdbData() throws IOException {
        List<Map<String, String>> collection = readCollection(fileImdbDataset);
        System.out.println("\nfirst document:");
        collection.get(0).forEach((key, value) -> System.out.println(String.format("%10s: %s", key, value)));
    }

    // analyzer demo
    // ----------------------------------------------------------------------------------------

    public static Analyzer getAnalyzer() {
        return new EnglishAnalyzer();
    }

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

    public static void printTokens(Analyzer analyzer, String text) throws IOException {
        TokenStream ts = analyzer.tokenStream("text", new StringReader(text));
        CharTermAttribute termAtt = ts.addAttribute(CharTermAttribute.class);

        for (ts.reset(); ts.incrementToken();)
            System.out.print(termAtt.toString() + " ");
        ts.end();
        System.out.println();
    }

    public static void runAnalyzerExample() throws IOException {
        String text = "I think text's values' color goes here; WHAT happens with it? do we see IT again; I went there to be gone with houses";
        CharArraySet stopWords = new CharArraySet(Arrays.asList("i", "do"), true);

        System.out.println("             text: " + text);
        System.out.println();

        // standard analyzer
        System.out.print("         standard: ");
        printTokens(new StandardAnalyzer(), text);

        // english analyzer (with porter stemmer)
        System.out.print("          english: ");
        printTokens(new EnglishAnalyzer(), text);

        // english analyzer (with porter stemmer) and new set of stopwords
        System.out.print("english/stopwords: ");
        printTokens(new EnglishAnalyzer(stopWords), text);

        // a custom analyzer, no lower case and kstemmer
        System.out.print("      my analyzer: ");
        printTokens(new MyAnalyzer(), text);

        // print standard stop word list
        System.out.println("\nenglish stopword list:");
        System.out.println(EnglishAnalyzer.getDefaultStopSet());
    }

    // build index
    // ----------------------------------------------------------------------------------------

    public static Directory getDirectory() throws IOException {
        return FSDirectory.open(Paths.get(pathIndex));
    }

    public static IndexWriter getIndexWriter() throws IOException {
        Directory directory = getDirectory();
        IndexWriterConfig config = new IndexWriterConfig(getAnalyzer());
        return new IndexWriter(directory, config);
    }

    public static void deleteIndex() throws IOException {
        IndexWriter writer = getIndexWriter();
        writer.deleteAll();
        writer.commit();
        writer.close();
    }

    public static Document createDocument(Map<String, String> data) {
        Document doc = new Document();

        // we store everything we need for result presentation
        doc.add(new TextField("title", data.get("title"), Field.Store.YES));
        doc.add(new IntField("year", Integer.parseInt(data.get("year")), Field.Store.YES));
        doc.add(new IntField("runtime", Integer.parseInt(data.get("runtime")), Field.Store.YES));
        doc.add(new FloatField("rating", Float.parseFloat(data.get("rating")), Field.Store.YES));

        // we do not store these fields and can't print them in the results
        doc.add(new TextField("actors", data.get("actors"), Field.Store.NO));
        doc.add(new TextField("genre", data.get("genre"), Field.Store.NO));
        doc.add(new TextField("summary", data.get("summary"), Field.Store.NO));

        return doc;
    }

    public static void loadBatch(List<Map<String, String>> docs) throws IOException {
        IndexWriter writer = getIndexWriter();

        for (Map<String, String> doc : docs)
            writer.addDocument(createDocument(doc));
        writer.close();
    }

    public static void loadImdbData(int batchSize) throws IOException {
        List<Map<String, String>> collection = readCollection(fileImdbDataset);

        deleteIndex();
        // load collection in batches do show how segments work
        for (int i = 0; i < collection.size(); i += batchSize)
            loadBatch(collection.subList(i, Math.min(i + batchSize, collection.size())));
    }

    // main function and demo dispatcher
    // ----------------------------------------------------------------------------------------

    public static void main(String[] args) throws IOException {
        // check on arguments and run parts of demo
        String action = args.length > 0 ? args[0].toLowerCase() : "analyze";

        // trigger action on first 3 letter
        if (action.startsWith("ana")) {
            System.out.println("IMDBSearch: running analyzer example");
            System.out.println();
            runAnalyzerExample();
        } else if (action.startsWith("sho")) {
            System.out.println("IMDBSearch: show imdb data");
            System.out.println();
            showImdbData();
        } else if (action.startsWith("loa")) {
            int batchSize = args.length > 1 ? Integer.parseInt(args[1]) : 100;
            System.out.println("IMDBSearch: load imdb data with batch size " + batchSize);
            System.out.println();
            loadImdbData(batchSize);
        } else
            System.out.println("IMDBSearch: unknown action `" + action + "`");
        System.out.println();
    }
}