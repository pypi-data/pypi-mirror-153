from torchvision.datasets.vision import VisionDataset
from IutyLib.file.files import CsvFile

from PIL import Image

def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


def accimage_loader(path):
    import accimage
    try:
        return accimage.Image(path)
    except IOError:
        # Potentially a decoding problem, fall back to PIL.Image
        return pil_loader(path)


def default_loader(path):
    from torchvision import get_image_backend
    if get_image_backend() == 'accimage':
        return accimage_loader(path)
    else:
        return pil_loader(path)

class FastCsvT1(VisionDataset):
    """
    find dataset from FastCNN/projects/{project}/{model}/DataSet.csv
    
    item type:
    path,dataset,tag  ->  E:/FastCNN/Projects/New_Project1/OK/image1.bmp, 训练集, OK
    """
    def _find_classes(self,data):
        classes = []
        for d in data:
            if not d[2] in classes:
                classes.append(d[2])
        return sorted(classes)
    
    def _make_dataset(self,data,classes,dataset):
        samples = []
        for d in data:
            if dataset == d[1]:
                idx = classes.index(d[2])
                if idx < 0:
                    continue
                item = d[0],idx
                samples.append(item)
        return samples
    
    def __init__(self, root,dataset = "训练集", transform=None,target_transform=None):
        super(FastCsvT1, self).__init__(root, transform=transform,target_transform=target_transform)
        
        csv = CsvFile("DataSet",root)
        data = csv.getData()
        
        self.classes = self._find_classes(data)
        
        self.samples = self._make_dataset( data, self.classes, dataset)
        if len(self.samples) == 0:
            raise (RuntimeError("Found 0 files in DataSet of: " + self.root))
    
    
    
    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        path, target = self.samples[index]
        sample = default_loader(path)
        if self.transform is not None:
            sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target

    def __len__(self):
        return len(self.samples)



if __name__ == "__main__":
    pass