depends = ('ITKPyBase', 'ITKIOImageBase', )
templates = (  ('ScancoImageIO', 'itk::ScancoImageIO', 'itkScancoImageIO', True),
  ('ScancoImageIOFactory', 'itk::ScancoImageIOFactory', 'itkScancoImageIOFactory', True),
)
factories = (("ImageIO","Scanco"),)
