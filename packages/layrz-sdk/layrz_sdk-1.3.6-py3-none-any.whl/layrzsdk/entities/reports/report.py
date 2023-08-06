""" Report class """
import time
import xlsxwriter
from .col import ReportDataType
from .format import ReportFormat
class Report:
  """
  Report definition

  Available attributes
  --------------------
    name (str): Report name. The exported name will have an timestamp to prevent duplicity in our servers.
    pages (list(ReportPage)): List of pages to append into report
    export_format (ReportFormat): Format to export the report
  """
  def __init__(self, name, pages, export_format):
    self.__name = name
    self.__pages = pages
    self.__export_format = export_format

  @property
  def name(self):
    """ Report name. The exported name will have an timestamp to prevent duplicity in our servers. """
    return self.__name

  @property
  def pages(self):
    """ List of pages to append into report """
    return self.__pages

  @property
  def export_format(self):
    """ export_format to export the report """
    return self.__export_format

  @property
  def filename(self):
    """ Report filename """
    return f'{self.name}_{int(time.time() * 1000)}.xlsx'

  @property
  def __readable(self):
    """ Readable property """
    return f'Report(name={self.name}, pages={self.pages}, export_format={self.export_format})'

  def __repr__(self):
    """ Readable property """
    return self.__readable

  def __str__(self):
    """ Readable property """
    return self.__readable

  def export(self, path):
    """ Export report to file """
    if self.export_format == ReportFormat.MICROSOFT_EXCEL:
      return self.__export_xlsx(path)
    else:
      raise Exception(f'Unsupported export format: {self.export_format}')

  def __export_xlsx(self, path):
    """ Export to Microsoft Excel (.xslx) """

    full_path = f'{path}/{self.filename}'
    book = xlsxwriter.Workbook(full_path)

    for page in self.pages:
      sheet = book.add_worksheet(page.name[0:31].replace('[', '').replace(']', ''))

      for i, header in enumerate(page.headers):
        style = book.add_format({
          'align': header.align.value,
          'font_color': header.text_color,
          'bg_color': header.color,
          'valign': 'vcenter',
          'font_size': 14,
          'top': 1,
          'left': 1,
          'right': 1,
          'bottom': 1,
          'font_name': 'Microsoft YaHei Light'
        })
        sheet.write(0, i, header.content, style)
        sheet.set_column(i, i, header.width)

      for i, row in enumerate(page.rows):
        for j, cell in enumerate(row.content):
          style = {
            'align': cell.align.value,
            'font_color': cell.text_color,
            'bg_color': cell.color,
            'valign': 'vcenter',
            'font_size': 10,
            'top': 1,
            'left': 1,
            'right': 1,
            'bottom': 1,
            'font_name': 'Microsoft YaHei Light'
          }

          if cell.data_type == ReportDataType.BOOL:
            value = 'Yes' if cell.value else 'No'
          elif cell.data_type == ReportDataType.DATETIME:
            value = cell.content.strftime(cell.datetime_format)
          elif cell.data_type == ReportDataType.INT:
            value = int(cell.content)
          elif cell.data_type == ReportDataType.FLOAT:
            value = float(cell.content)
            style.update({'num_format': '0.00'})
          elif cell.data_type == ReportDataType.CURRENCY:
            value = float(cell.content)
            style.update({'num_format': f'"{cell.currency_symbol}" * #,##0.00;[Red]"{cell.currency_symbol}" * #,##0.00'})
          else:
            value = cell.content

          sheet.write(i + 1, j, value, book.add_format(style))

          if row.compact:
            sheet.set_row(i + 1, None, None, {'level': 1, 'hidden': True})
          else:
            sheet.set_row(i + 1, None, None, {'collapsed': True})
    book.close()

    return full_path
