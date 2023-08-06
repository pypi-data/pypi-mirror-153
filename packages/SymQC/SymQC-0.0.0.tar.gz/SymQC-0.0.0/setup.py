from setuptools import setup, find_packages

setup(
    name="SymQC",
    version="0.0.0",
    keywords=["pip", "SymQC", "symbolic computation", "quantum simulator"],
    description="Quantum computing simulator",
    long_description="Quantum computing simulator based on symbolic computing",
    license="MIT Licence",

    url="https://gitee.com/quingo/SymQc",
    author="hpcl_quanta",
    author_email="1245949348@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["sympy", "ply"]
)
