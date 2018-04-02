# Makefile for creating Concrete ACE 2005 with
# annotations from Stanford and Chunklink.
#
# TODO: Change all concrete directories from "comms" to "concrete".
#

SHELL = /bin/bash
JAVAIN = export CLASSPATH=`mvn -f ./scripts/maven/pom-acex3.xml exec:exec -q -Dexec.executable="echo" -Dexec.args="%classpath"` && java
# JAVAIN = export CLASSPATH=`mvn -f /mnt/d/MyProjects/acex3/pom.xml exec:exec -q -Dexec.executable="echo" -Dexec.args="%classpath"` && java
JAVACS = export CLASSPATH=`mvn -f ./scripts/maven/pom-cs.xml exec:exec -q -Dexec.executable="echo" -Dexec.args="%classpath"` && java
PYTHON = python
JAVAFLAGS = -ea

CONCRETE_CHUNKLINK=./concrete-chunklink

# Machine specific parameters.
LDC_DIR=/mnt/d/MyProjects/ACE2005
OUT_DIR=/mnt/d/MyProjects/ACE2005/preprocess
JAVAFLAGS = -ea -Xmx4096m -XX:-UseParallelGC -XX:-UseParNewGC -XX:+UseSerialGC
########
# Error if LDC_DIR and OUT_DIR weren't defined on the command line.
ifndef LDC_DIR
$(error The variable LDC_DIR should be defined on the command line)
endif
ifndef OUT_DIR
$(error The variable OUT_DIR should be defined on the command line)
endif
#######
endif

# ACE 2005 variables.
ACE_OUT_DIR=$(abspath $(OUT_DIR))
LDC2006T06=$(abspath $(LDC_DIR))/LDC2006T06
LDC2006T06_EN=$(abspath $(LDC_DIR))/LDC2006T06/data/English
LDC2006T06_EN_SYM=$(ACE_OUT_DIR)/LDC2006T06_temp_copy
ACE05_COMMS=$(ACE_OUT_DIR)/ace-05-comms
ACE05_ANNO=$(ACE_OUT_DIR)/ace-05-comms-ptb-anno
ACE05_CHUNK=$(ACE_OUT_DIR)/ace-05-comms-ptb-anno-chunks
ACE05_SPLITS=$(ACE_OUT_DIR)/ace-05-splits
APF_XML_FILES =$(notdir $(wildcard $(LDC2006T06_EN)/*/adj/*.apf.xml)) 

.PHONY: all
all: 
	$(info "This Makefile should be run once: 'make ace05splits'.) 

.PHONY: anno
anno: ace05splits

# ----------------------------------------------------------------
# Install (clone) concrete-chunklink from GitHub
# ----------------------------------------------------------------
setup: $(CONCRETE_CHUNKLINK)
	$(JAVAIN) -version
	$(JAVACS) -version

$(CONCRETE_CHUNKLINK):
	pip install 'concrete>=4.4.0,<4.8.0'
	git clone https://github.com/mgormley/concrete-chunklink.git $(CONCRETE_CHUNKLINK)
	cd $(CONCRETE_CHUNKLINK) && git checkout v0.2

# ----------------------------------------------------------------
# ACE 2005 Data
# ----------------------------------------------------------------

# Checks that the LDC directory exits.
$(LDC2006T06):
	$(error "LDC directory does not exist: $(LDC2006T06)")

# Copy over the required .dtd files.
$(LDC2006T06_EN_SYM)/apf.v5.1.1.dtd: $(LDC2006T06)/dtd/apf.v5.1.1.dtd
	mkdir -p $(dir $@)
	ln -s $< $@ || true

# Create a flat symlinks only copy of the LDC directory.
# (This is done so that we can move the dtd files into the correct place.)
$(LDC2006T06_EN_SYM)/%.apf.xml: $(LDC2006T06_EN)/*/adj/%.apf.xml $(LDC2006T06_EN)/*/adj/%.sgm
	mkdir -p $(dir $@)
	ln -s $^ $(dir $@) || true

# Converts the ACE 2005 data to Concrete Communications.
$(ACE05_COMMS)/%.concrete: $(LDC2006T06_EN_SYM)/%.apf.xml $(LDC2006T06_EN_SYM)/apf.v5.1.1.dtd
	mkdir -p $(ACE05_COMMS)
	$(JAVAIN) $(JAVAFLAGS) edu.bit.nlp.concrete.ingesters.acex3.AceApf2Concrete $< $@ 

# Annotates the ACE Communications with concrete-stanford.
$(ACE05_ANNO)/%.concrete : $(ACE05_COMMS)/%.concrete
	mkdir -p $(ACE05_ANNO)
	$(JAVACS) $(JAVAFLAGS) edu.jhu.hlt.concrete.stanford.AnnotateTokenizedConcrete $< $@

# Converts the parses from concrete-stanford to chunks with concrete-chunklink.
$(ACE05_CHUNK)/%.concrete : $(ACE05_ANNO)/%.concrete $(CONCRETE_CHUNKLINK)
	mkdir -p $(ACE05_CHUNK)
	$(PYTHON) $(CONCRETE_CHUNKLINK)/concrete_chunklink/add_chunks.py --chunklink $(CONCRETE_CHUNKLINK)/scripts/chunklink_2-2-2000_for_conll.pl $< $@

# Converts all the ACE 2005 data to Concrete Communications.
.PHONY: ace05comms
ace05comms: $(addprefix $(ACE05_COMMS)/,$(subst .apf.xml,.concrete,$(APF_XML_FILES)))

# Annotates all of the ACE 2005 data with Stanford tools and chunklink.pl.
.PHONY: ace05anno
ace05anno: $(addprefix $(ACE05_CHUNK)/,$(subst .apf.xml,.concrete,$(APF_XML_FILES)))

# Split the annotated ACE Concrete files into domains.
.PHONY: ace05splits
ace05splits: $(LDC2006T06) ace05anno
	bash ./scripts/data/split_ace_dir.sh $(LDC2006T06) $(ACE05_CHUNK) $(ACE05_SPLITS)/comms concrete

# Don't delete intermediate files.
.SECONDARY:

.SILENT: clean
.PHONY: clean
clean :
	-@rm -r $(ACE_OUT_DIR)
