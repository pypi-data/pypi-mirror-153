import midas
import time


def main():

    t_start = time.time()
    midas.run(
        "four_bus",
        params={
            "mosaikdb_params": {
                "filename": "mosaikhdf.hdf5",
            },
            "with_db": True,
            "end": 30 * 24 * 60 * 60,
        },
    )
    t_mnt = time.time() - t_start
    print(f"MosaikHDF5: {t_mnt:.3f}")

    t_start = time.time()
    midas.run(
        "four_bus",
        params={
            "mosaikdb_params": {
                "import_str": "midas.core.store:MidasHdf5",
                "filename": "no_threads.hdf5",
                "buffer_size": 0,
            },
            "with_db": True,
            "end": 30 * 24 * 60 * 60,
        },
    )
    t_mnt = time.time() - t_start
    print(f"MidasStore without threads: {t_mnt:.3f}")

    t_start = time.time()
    midas.run(
        "four_bus",
        params={
            "mosaikdb_params": {
                "import_str": "midas.core.store:MidasHdf5",
                "filename": "large_threads.hdf5",
                "buffer_size": 1000,
            },
            "with_db": True,
            "end": 30 * 24 * 60 * 60,
        },
    )
    t_mnt = time.time() - t_start
    print(f"MidasStore with large buffer: {t_mnt:.3f}")

    t_start = time.time()
    midas.run(
        "four_bus",
        params={
            "mosaikdb_params": {
                "import_str": "midas.core.store:MidasHdf5",
                "filename": "small_threads.hdf5",
                "buffer_size": 100,
            },
            "with_db": True,
            "end": 30 * 24 * 60 * 60,
        },
    )
    t_mnt = time.time() - t_start
    print(f"MidasStore with small buffer: {t_mnt:.3f}")


if __name__ == "__main__":
    main()
