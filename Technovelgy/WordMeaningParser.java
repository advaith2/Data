import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

/**
 * @author anandh
 *	Parser Program to parse the web-site Technovelgy.com
 */
public class WordMeaningParser 
{
	private Workbook wb;
	private Sheet sheet;
	private int row_count;
	public WordMeaningParser(String fileName)
	{
		long start_time = System.currentTimeMillis();
		initWorkBook();
		master_page_starter();
		System.out.println("Writing Contents to File");
		writeToFile(fileName);
		print_TimeTaken(System.currentTimeMillis()-start_time);
	}
	/**
	 * Creating a workbook and worksheet
	 * Initializing and adding title for the Sheet in the Workbook
	 */
	public void initWorkBook()
	{
		row_count=0;
		wb = new XSSFWorkbook();
		sheet=wb.createSheet("Technovelgy");
		Row row = sheet.createRow(row_count++);
		CellStyle cellStyle = wb.createCellStyle();
		Font f = wb.createFont();
		f.setBold(true);
		cellStyle.setFont(f);
		Cell temp_cell = row.createCell(0);
		temp_cell.setCellValue("Device Name");
		temp_cell.setCellStyle(cellStyle);
		temp_cell = row.createCell(1);
		temp_cell.setCellValue("Story");
		temp_cell.setCellStyle(cellStyle);
		temp_cell = row.createCell(2);
		temp_cell.setCellValue("Author");
		temp_cell.setCellStyle(cellStyle);
		temp_cell = row.createCell(3);
		temp_cell.setCellValue("Date");
		temp_cell.setCellStyle(cellStyle);
		temp_cell = row.createCell(4);
		temp_cell.setCellValue("Sentence");
		temp_cell.setCellStyle(cellStyle);
	}
	/**
	 * @param time
	 * Function to print the time taken in minutes and seconds for a given time difference
	 */
	public void print_TimeTaken(long time)
	{
		System.out.println(String.format("%d min, %d sec", 
			    TimeUnit.MILLISECONDS.toMinutes(time),
			    TimeUnit.MILLISECONDS.toSeconds(time) - 
			    TimeUnit.MINUTES.toSeconds(TimeUnit.MILLISECONDS.toMinutes(time))
			));
	}
	/**
	 * Iterates the index page for each alphabet
	 */
	public void master_page_starter()
	{
		for (char alphabet = 'A'; alphabet <= 'Z';alphabet++)
		{
			System.out.println("Alphabet "+alphabet+" in progress");
			try 
			{
				getAlphabetDetails("http://www.technovelgy.com/ct/ctnlistalpha.asp?FL="+alphabet);
			}
			catch (IOException e) 
			{
				e.printStackTrace();
			}
			catch (InterruptedException e) 
			{
				e.printStackTrace();
			}
		}
	}
	/**
	 * @param fileName
	 * Writes the workbook to a specified file
	 */
	public void writeToFile(String fileName)
	{
		FileOutputStream fileOut = null;
		try 
		{
			fileOut = new FileOutputStream(fileName);
			wb.write(fileOut);
		}
		catch (FileNotFoundException e) 
		{
			e.printStackTrace();
		}
		catch (IOException e) 
		{
			e.printStackTrace();
		}
		finally
		{
			if(fileOut!=null)
			{
				try 
				{
					fileOut.close();
				}
				catch (IOException e) 
				{
					e.printStackTrace();
				}
			}
		}
	}
	/**
	 * @param device_name
	 * @param story
	 * @param author
	 * @param date
	 * @param sentence
	 * Inserting a particular row in the worksheet
	 */
	public void insert_data(String device_name, String story, String author, String date, String sentence)
	{
		Row row = sheet.createRow(row_count++);
		row.createCell(0).setCellValue(device_name);
		row.createCell(1).setCellValue(story);
		row.createCell(2).setCellValue(author);
		row.createCell(3).setCellValue(date);
		row.createCell(4).setCellValue(sentence);
	}
	/**
	 * @param url
	 * @return
	 * @throws InterruptedException
	 * Parses the html given by the url and gets the sentence in which the word is used
	 */
	public String getContents(String url) throws InterruptedException
	{
		Document doc=null;
		int retry_count=0;
		while(retry_count<3)
		{
			try 
			{
				doc = Jsoup.connect(url).get();
				break;
			}
			catch (IOException e) 
			{
				retry_count++;
				Thread.sleep(200);
				System.out.println("Retrying for URL: "+url);
			}
		}
		Element ele = doc.select("table").get(3).select("tr").get(0).select("td").get(0);
		return ele.text();
	}
	/**
	 * @param url
	 * @throws IOException
	 * @throws InterruptedException
	 * Gets all the words from the starting page for a particular alphabet
	 */
	public void getAlphabetDetails(String url) throws IOException, InterruptedException
	{
		int count =0;
		Document doc = Jsoup.connect(url).get();
		Element ele = doc.select("table").get(2);
		for(Element elem: ele.select("tr"))
		{
			if(count ==0)
			{
				count++;
				continue;
			}
			insert_data(elem.select("td").get(0).text(),elem.select("td").get(1).text(),
					elem.select("td").get(2).text(), elem.select("td").get(3).text(),
					getContents(elem.select("a[href]").attr("abs:href")));
		}
	}
	/**
	 * @param args
	 * Main
	 */
	public static void main(String[] args) 
	{
		new WordMeaningParser("/home/anandh/Documents/ScienceFiction-master/technovelgy.xlsx");
	}
}
