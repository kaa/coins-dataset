# coins-dataset
A dataset of euro coin images classified by denomination

## Structure
The data set is structured suitable to read using Keras `ImageDataGenerator.flow_from_directory()` method.

    .
    ├── extract.py              # Python script used to extract coins from images
    ├── src                     # Source images
    |   └── ...    
    └── classified              # Classified example images
        ├── train               # Training set, structured according to denomination
        |   ├── 2c
        |   └── ...
        └── test                # Test or validation set
            └── ...

## Contributing

I'd be happy to accept corrections or additions to the dataset. Please make sure to follow 
the general style and dimensions of the existing data.

Source images are shot top-down on an A4 sized white background with soft ambient lighting. The source images
are then post-processed using the supplied `extract.py` file to isolate individual coins and normalize the sizes
before manual classification.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
